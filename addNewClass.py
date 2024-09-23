from json import load
from exec import exec
from actualize import actualize
import os
import requests
c = input("What class do you wanna add ?")

if os.path.exists("classes.txt") and any([c == l.split('|')[0] for l in open("classes.txt").readlines()]):
    print("This class already exists")
else:
    if not os.path.exists("groups.json"):
        f = open("groups.json", "w")
        def officeLogin():
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
        
        def getGroups(token):
            url = "https://zeus.ionis-it.com/api/group/"
            headers = {"Authorization": "Bearer " + token}
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                return response.text
            else:
                print("Request error: code", response.status_code, ", endpoint", url)
        f.write(getGroups(officeLogin()))
        f.close()
        
    groups = load(open("groups.json"))
    groups = [g for g in groups if g["name"] == c]
    if len(groups) == 0:
        print("No group with such name found")
    elif len(groups) > 1:
        print("Too many groups found")
        print(groups)
    else:
        g = groups[0]
        calendar = {
            'summary': c,
            'timeZone': 'Europe/Paris'
        }
        calId = exec(lambda service: service.calendars().insert(body=calendar).execute())['id']
        f = open("classes.txt", "a")
        f.write(f"\n{c}|{g['id']}|{calId}")
        f.close()
        exec(lambda x: actualize(x, (g['id'], calId)))
