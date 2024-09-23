from time import sleep
import os

def deleteEverything(service):
    for l in open("classes.txt").readlines():
        # batch = service.new_batch_http_request()
        c, gid, calId = l.removesuffix("\n").split("|")
        print(c)
        page_token = None
        while True:
            events = service.events().list(calendarId=calId, pageToken=page_token).execute()
            for event in events['items']:
                # batch.add(
                service.events().delete(
                    calendarId=calId,
                    eventId=event["id"]
                ).execute()
                # )
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        # batch.execute()
        if os.path.exists("ids_list" + gid + ".txt"):
            os.remove("ids_list" + gid + ".txt")