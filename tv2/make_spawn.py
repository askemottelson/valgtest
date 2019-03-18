# python3 make_spawn.py > spawn.sh

import os.path

c = 0
for i in range(0, 10000):

    if os.path.isfile("data/data" + str(i) + ".json"):
        continue
    
    c += 1

    if c % 10 == 0:
        print("python3 go.py "+str(i))        
        print("sleep 30")
    else:
        print("python3 go.py "+str(i)+" &")

