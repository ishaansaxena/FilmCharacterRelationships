import json

with open('cvd.json') as f:
    d = json.load(f)

with open('cvsd.json') as f:
    e = json.load(f)

for k, v in e.items():
    if k in d:
        d[k].extend(v)
    else:
        d[k] = v
    
with open('cv.json', 'w') as f:
    json.dump(d, f)
