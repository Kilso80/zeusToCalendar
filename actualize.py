from eventGetter import ZeusEventGetter
from datetime import datetime
import os

def actualize(service, group):
    idslist = {}
    gid = group[0]
    calId = group[1]
    def creationCallback(request_id, response, exception):
        if response is None: print(exception)
        idslist[response["description"]] = response["id"], response["start"]["dateTime"][:10]

    count = [0, 0]
    batch = service.new_batch_http_request()
    eventList = ZeusEventGetter(gid).eventList
    if os.path.exists(f"ids_list{gid}.txt"):
        uids2ids = {k: (v, dt.removesuffix("\n")) for k, v, dt in [l.split('|') for l in open(f"ids_list{gid}.txt").readlines()]}
    else: 
        uids2ids = dict()
    for event in eventList:
        if event["description"] in uids2ids:
            idslist[event["description"]] = uids2ids[event["description"]]
            uids2ids.pop(event["description"])
        else:
            batch.add(
                service.events().insert(
                    calendarId=calId,
                    body=event
                ),
                creationCallback
            )
            count[0] += 1
    today = datetime.now().strftime("%Y-%m-%d")
    for id, dt in uids2ids.values():
        if dt >= today:
            count[1] += 1
            batch.add(
                service.events().delete(
                    calendarId=calId,
                    eventId=id
                )
            )
    batch.execute()
    f = open(f"ids_list{gid}.txt", "w")
    f.write("\n".join([uid + "|" + id + "|" + dt[:10] for uid, (id, dt) in idslist.items()]))
    f.close()
    print(count[0], "events created,", count[1], "deleted")