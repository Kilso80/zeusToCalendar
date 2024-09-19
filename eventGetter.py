import requests
from datetime import datetime

class ZeusEventGetter:
    def __init__(self, gid):
        self.token = self.officeLogin()
        self.groupId = gid
        cList = self.getCourses(self.groupId)
        self.eventList = [self.parseEvent(e) for e in self.getEventList(cList)]
    
    def officeLogin(self):
        url = "https://zeus.ionis-it.com/api/User/OfficeLogin"
        # https://developer.microsoft.com/en-us/graph/graph-explorer to get office token
        payload = {"accessToken": open("office_token.txt").read()}
        headers = {
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("Login error: code", response.status_code)

    def getCourses(self, groupId, begin=None):
        if begin is None:
            begin = datetime.now().strftime("%Y-%m-%d")
        url = "https://zeus.ionis-it.com/api/group/" + str(groupId) + "/ics?startDate=" + begin
        headers = {"Authorization": "Bearer " + self.token}
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print("Request error: code", response.status_code, ", endpoint", url)

    def getEventList(self, textEvents: str):
        events = textEvents.removesuffix("\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n").split("\r\nEND:VEVENT\r\nBEGIN:VEVENT\r\n")
        events[0] = events[0].split("BEGIN:VEVENT\r\n")[1]
        return events

    def parseEvent(self, event):
        event = event.encode('latin1').decode('utf-8')
        event = {k: v for k, v in [e.split(':') for e in event.replace("\r\n ", "").split("\r\n")]}
        convertTime = lambda t: datetime.strptime(t, "%Y%m%dT%H%M%SZ").strftime("%Y-%m-%dT%H:%M:%SZ")
        return {
            'summary': event["SUMMARY"],
            'location': event["LOCATION"].replace('\\', ''),
            'description': event["UID"],
            'start': {
                'dateTime': convertTime(event["DTSTART"]),
                'timeZone': 'Europe/Paris',
            },
            'end': {
                'dateTime': convertTime(event["DTEND"]),
                'timeZone': 'Europe/Paris',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 10},
                ],
            }
        }
