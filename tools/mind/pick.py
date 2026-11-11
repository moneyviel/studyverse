import json,sys,collections
t=sys.argv[1]; d=json.load(open(f'../../content/mind/{t}.json'))['questions']
L=[q for q in d if len(q['o'][0])==max(len(o) for o in q['o'])]
need=len(L)-int(0.33*len(d))
by=collections.defaultdict(list)
for q in L: by[q['b']].append(q)
pick=[]
for b,qs in by.items():
    k=round(need*len(qs)/len(L)); pick+=qs[:k]
print(t,'longest',len(L),'fix',len(pick))
for q in pick: print(f"{q['id']}|{q['q']}|B:{q['o'][0]}|1:{q['o'][1]}|2:{q['o'][2]}|3:{q['o'][3]}")
