from time import sleep

def deleteEverything(service):
    for l in open("classes.txt").readlines():
        batch = service.new_batch_http_request()
        c, gid, calId = l.removesuffix("\n").split("|")
        print(c)
        page_token = None
        while True:
            events = service.events().list(calendarId=calId, pageToken=page_token).execute()
            for event in events['items']:
                batch.add(
                service.events().delete(
                    calendarId=calId,
                    eventId=event["id"]
                ))
            page_token = events.get('nextPageToken')
            if not page_token:
                break
        batch.execute()
        f = open("ids_list" + gid + ".txt", "w")
        f.write('')
        f.close()
        print("Done, waiting...")
        sleep(30)