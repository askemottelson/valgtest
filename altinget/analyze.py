import glob
import json
from collections import Counter

master = []

for file in glob.glob("data/*.json"):
    with open(file) as f:
        data = json.load(f)

        master.extend(data)

print("tests:", len(master))

d = {}
for run in master:
    q = run['result']['top1']['parti']
    if not q in d:
        d[q] = 0
    d[q] += 1

for key in d.keys():
    d[key] = d[key] / len(master) * 100.0

    print(key, d[key])



## kandidat
d = []
for run in master:
    q = run['result']['top1']['name'] + ", " + run['result']['top1']['parti']
    d.append(q)

cnt = Counter()
for name, count in Counter(d).most_common(100):
    print(name, count/len(d), "%")