import json,os,urllib.request as ur
V={".":0,"p":100,"n":320,"b":330,"r":500,"q":950,"k":0}
T={"p":"kkkklmmgljikkkkollmpmmoquuuukkkk","n":"aceecgklelmneknoelmncgkkcgklacee"}
T={p:[(ord(s[(i>>3)*4+min(i&7,7-i&7)])-97)*5-50 for i in range(64)]for p,s in T.items()}
for z in"brqk":T[z]=[0]*64
ND=(14,31,33,18,-14,-31,-33,-18);BD=(15,17,-15,-17);RD=(1,16,-1,-16);KD=BD+RD;RM={0:2,7:1,112:8,119:4}
MATE=10**5;NODES=[0]
def A(B,t,w):
 s=B[0]
 for j,ds in enumerate((((-15,-17)if w else(15,17)),ND,KD)):
  pc=("pnk","PNK")[w][j]
  for d in ds:
   x=t+d
   if not x&136 and s[x]==pc:return 1
 for d in KD:
  ks="BQ"if d in BD else"RQ";x=t+d
  while not x&136:
   p=s[x]
   if p!=".":
    if p.isupper()==w and p.upper()in ks:return 1
    break
   x+=d
 return 0
def parse(fen):
 f=fen.split();s=["."]*128;i=112
 for c in f[0]:
  if c.isdigit()or c=="/":i+=int(c)if c.isdigit()else-24
  else:s[i]=c;i+=1
 c=f[2]
 cast=sum(1<<i for i,ch in enumerate("KQkq")if ch in c)
 ep=-1if f[3]=="-"else ord(f[3][0])-97+(int(f[3][1])-1)*16
 return[s,f[1],cast,ep]
def mk(B,m):
 fr,to,pr=m;s=B[0][:];pc=s[fr];cast=B[2];ep=-1
 if pc.upper()=="P"and to==B[3]and fr%16!=to%16:s[to-16if pc.isupper()else to+16]="."
 s[to]=pr if pr else pc;s[fr]="."
 if pc.upper()=="P"and abs(to-fr)==32:ep=(to+fr)//2
 if pc.upper()=="K"and abs(to-fr)==2:
  rf,rt=(fr+3,fr+1)if to>fr else(fr-4,fr-1);s[rt]=s[rf];s[rf]="."
 if pc.upper()=="K":cast&=~(3if pc=="K"else 12)
 cast&=~(RM.get(fr,0)|RM.get(to,0))
 return[s,"b"if B[1]=="w"else"w",cast,ep]
def pm(out,i,t,w):
 if t//16==(7if w else 0):out.extend((i,t,pr.upper()if w else pr)for pr in"qrbn")
 else:out.append((i,t,""))
def G(B,w):
 s=B[0];out=[]
 for i,p in enumerate(s):
  if p=="."or p.isupper()!=w:continue
  u=p.upper()
  if u=="P":
   up=16if w else-16;o=i+up
   if s[o]==".":
    pm(out,i,o,w)
    if i//16==(1if w else 6)and s[i+2*up]==".":out.append((i,i+2*up,""))
   for d in(up-1,up+1):
    t=i+d
    if t&136:continue
    if s[t]!="."and s[t].isupper()!=w:pm(out,i,t,w)
    elif t==B[3]:out.append((i,t,""))
  elif u in"NK":
   for d in(ND if u=="N"else KD):
    t=i+d
    if not t&136 and(s[t]=="."or s[t].isupper()!=w):out.append((i,t,""))
  else:
   for d in(BD if u=="B"else RD if u=="R"else KD):
    t=i+d
    while not t&136:
     q=s[t]
     if q=="."or q.isupper()!=w:out.append((i,t,""))
     if q!=".":break
     t+=d
 h=4if w else 116
 if s[h]==("K"if w else"k"):
  for sg,bt,rq,em,tr in((1,1if w else 4,h+3,(1,2),(0,1,2)),(-1,2if w else 8,h-4,(-1,-2,-3),(0,-1,-2))):
   if B[2]&bt and s[rq]==("R"if w else"r")and all(s[h+k]=="."for k in em)and not any(A(B,h+k,not w)for k in tr):out.append((h,h+2*sg,""))
 return out
def IL(B2,w):
 return A(B2,B2[0].index("K"if w else"k"),not w)
def E(B):
 s=B[0];tot=0
 for i,p in enumerate(s):
  if p==".":continue
  r,f=i>>4,i&15;q=p.lower()
  if p.isupper():tot+=V[q]+T[q][r*8+f]
  else:tot-=V[q]+T[q][(7-r)*8+f]
 return tot if B[1]=="w"else-tot
def S(B,d,a,b):
 NODES[0]+=1;w=B[1]=="w";s=B[0]
 if NODES[0]>=80000:return E(B)
 if d<=0:
  st=E(B)
  if st>=b:return b
  if st>a:a=st
  ms=[m for m in G(B,w)if s[m[1]]!="."or m[2]]
 else:ms=G(B,w)
 ms.sort(key=lambda m:V[s[m[0]].lower()]-10*V[s[m[1]].lower()]);best=-2*MATE
 for m in ms:
  B2=mk(B,m)
  if IL(B2,w):continue
  sc=-S(B2,d-1,-b,-a)
  if sc>best:best=sc
  if sc>a:a=sc
  if a>=b:break
 if d<=0:return a
 if best==-2*MATE:return-MATE if A(B,s.index("K"if w else"k"),not w)else 0
 return best
def nm(i):
 return chr(97+i%16)+chr(49+i//16)
def C(fen):
 B=parse(fen);w=B[1]=="w";ms=[m for m in G(B,w)if not IL(mk(B,m),w)]
 NODES[0]=0;ss=[(-S(mk(B,m),0,-2*MATE,2*MATE),m)for m in ms];ss.sort()
 al=-2*MATE
 for _,m in ss[:-7:-1]:
  NODES[0]=62000;sc=-S(mk(B,m),4,-2*MATE,-al)
  if sc>al:al,bm=sc,m
 return nm(bm[0])+nm(bm[1])+bm[2].lower()
def post(path,body):
 return json.load(ur.urlopen(ur.Request(os.getenv("MAKEFUN_ENV_URL")+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})))
g={"status":""}
while g["status"]!="done":
 g=post("/game",{})
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":C(g["fen"])})
