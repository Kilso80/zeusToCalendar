from actualize import actualize
from deleteEverything import deleteEverything
from time import sleep
from exec import exec

# 2 functions available: actualize or deleteEverything
# exec(deleteEverything)

for l in open("classes.txt").readlines():
    c, gid, calId = l.removesuffix("\n").split('|')
    gid = int(gid)
    exec(lambda x: actualize(x, (gid, calId)))
    print(c, 'done')
    sleep(30)