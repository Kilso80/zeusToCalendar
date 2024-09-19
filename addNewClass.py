from json import load
from exec import exec
c = input("What class do you wanna add ?")

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
    print("Ok done")
