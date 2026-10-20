import json,time,sys,urllib.request,datetime
B="https://sinfralog.sinfra.mt.gov.br/obrasgov-map-backend/source/seinfra"
H={"User-Agent":"Mozilla/5.0"}
def get(p,body=None,tries=3):
    for i in range(tries):
        try:
            h=dict(H)
            if body is not None: h["Content-Type"]="application/json"
            r=urllib.request.Request(B+p,data=body,headers=h)
            with urllib.request.urlopen(r,timeout=60) as x: return json.load(x)
        except Exception as e:
            if i==tries-1: raise
            time.sleep(3)
filt=get("/app/filters")
lista=get("/contract/list",json.dumps(filt).encode())
vig=[c for c in lista if c.get("status")=="Vigente"]
print(len(lista),"contratos,",len(vig),"vigentes")
if len(vig)<50:
    sys.exit("Poucos contratos vigentes; mantendo o painel.json anterior.")
out=[]
for c in vig:
    try: d=get("/contract/%s"%c["id"])
    except Exception: continue
    p=d.get("period") or {}
    if not p.get("initialDate") or not p.get("finalDate"): continue
    lat=lng=None
    for k in d.get("construction") or []:
        for q in k.get("coordinate") or []:
            if q.get("nuLatitude"): lat,lng=q["nuLatitude"],q["nuLongitude"]; break
        if lat: break
    out.append(dict(name=d["name"],status=d.get("status"),address=c.get("address",""),
        company=(d.get("companies") or [""])[0],value=d.get("contractTotalValue") or 0,
        ini=p["initialDate"],fim=p["finalDate"],ex=round(d.get("peExecutedAmount") or 0),
        pg=round(d.get("pePaidAmount") or 0),lat=lat,lng=lng))
    time.sleep(0.2)
if len(out)<50: sys.exit("Coleta incompleta; mantendo o painel.json anterior.")
json.dump({"updated":datetime.datetime.utcnow().isoformat()+"Z","items":out},open("painel.json","w"),ensure_ascii=False)
print("OK",len(out))
