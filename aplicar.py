import sys
lines=open(sys.argv[1],encoding="utf-8").read().split("\n")
cur=None;mode=None;old=[];new=[];ops=[]
for l in lines:
    if l.startswith("@@@ARQ "): cur=l[7:].strip();continue
    if l=="@@@OLD": mode="o";old=[];continue
    if l=="@@@NEW": mode="n";new=[];continue
    if l=="@@@END": ops.append((cur,"\n".join(old),"\n".join(new)));mode=None;continue
    if mode=="o": old.append(l)
    elif mode=="n": new.append(l)
ok=True;cache={}
for f,o,n in ops:
    s=cache[f] if f in cache else open(f,encoding="utf-8").read()
    c=s.count(o)
    if c!=1:
        print("FALHOU",f,c,"ocorrencias:",o[:60]);ok=False;continue
    cache[f]=s.replace(o,n)
if ok:
    for f,s in cache.items(): open(f,"w",encoding="utf-8").write(s)
    print("aplicado:",len(ops),"alteracoes")
else:
    print("NADA FOI ALTERADO")
