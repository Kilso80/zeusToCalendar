from eventGetter import ZeusEventGetter
from datetime import datetime
import os

def actualize(service, group):
    idslist = {}
    gid = group[0]
    calId = group[1]
    def creationCallback(request_id, response, exception):
        if response is None: print(exception)
        idslist[response["description"].split("\n")[0]] = response["id"], response["start"]["dateTime"][:10], response["description"].split("\n")[1]

    count = [0, 0, 0]
    # batch = service.new_batch_http_request()
    eventList = ZeusEventGetter(gid).eventList
    if os.path.exists(f"ids_list{gid}.txt"):
        uids2ids = {k: (v, dt, modified.removesuffix("\n")) for k, v, dt, modified in [l.split('|') for l in open(f"ids_list{gid}.txt").readlines()]}
    else: 
        uids2ids = dict()
    for event in eventList:
        uid = event["description"].split('\n')[0]
        if uid in uids2ids:
            if uids2ids[uid][2] != event["description"].split("\n")[1]:
                uids2ids.pop(uid)
                service.events().delete(
                    calendarId=calId,
                    eventId=id
                ).execute()
                creationCallback(None, service.events().insert(
                    calendarId=calId,
                    body=event).execute(), None)
                count[2] += 1
            else:
                idslist[uid] = uids2ids.pop(uid)
            
        else:
            # batch.add(
            #     service.events().insert(
            #         calendarId=calId,
            #         body=event
            #     ),
            #     creationCallback
            # )
            creationCallback(None, service.events().insert(
                    calendarId=calId,
                    body=event).execute(), None)
            count[0] += 1
    today = datetime.now().strftime("%Y-%m-%d")
    for id, dt, mts in uids2ids.values():
        if dt >= today:
            count[1] += 1
            # batch.add(
            service.events().delete(
                calendarId=calId,
                eventId=id
            ).execute()
            # )
    # batch.execute()
    f = open(f"ids_list{gid}.txt", "w")
    f.write("\n".join([uid + "|" + id + "|" + dt[:10] + "|" + mts for uid, (id, dt, mts) in idslist.items()]))
    f.close()
    print(count[0], "events created,", count[1], "deleted,", count[2], "modified")
