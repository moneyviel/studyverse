import sys,os,re
t=sys.argv[1]; rows=[l.rstrip('\n') for l in open(f'{t}.txt',encoding='utf-8')]
idx=[i for i,l in enumerate(rows) if l.strip() and not l.startswith('#')]
n=0
for p in open(f'{t}.patch',encoding='utf-8'):
    p=p.strip()
    if not p: continue
    qid,k,txt=p.split('|',2); num=int(qid.rsplit('-',1)[1])-1
    f=rows[idx[num]].split('|'); assert f[0]==qid.split('-')[1], qid
    assert 1<=int(k)<=3 and '|' not in txt
    f[2+int(k)]=txt; rows[idx[num]]='|'.join(f); n+=1
open(f'{t}.txt','w',encoding='utf-8').write('\n'.join(rows)+'\n'); print(t,'patched',n)
