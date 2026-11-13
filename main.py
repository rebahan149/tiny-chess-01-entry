import json,os,urllib.request as ur
V=dict(zip(".pnbrqk",(0,100,320,330,500,950,0)))
T={"p":"kkkklmmgljikkkkollmpmmoquuuukkkk","n":"aceecgklcgkkelmneknoelmncgklacee","k":"oqmkookkiggggeececcaeccaeccageec"}
T={p:[V[p]+(ord(c)-97)*5-50 for c in s]for p,s in T.items()}
ND=(14,31,33,18,-14,-31,-33,-18);BD=(15,17,-15,-17);RD=(1,16,-1,-16);KD=BD+RD;RM={0:2,7:1,112:8,119:4}
MATE=10**5;N=[0,100000];TT={}
def A(B,t,w):
 s=B[0]
 for ds,pc in zip((((-15,-17)if w else(15,17)),ND,KD),("pnk","PNK")[w]):
  for d in ds:
   x=t+d
   if not x&136 and s[x]==pc:return 1
 for d,ks in zip(KD,["BQ"]*4+["RQ"]*4):
  x=t+d
  while not x&136:
   p=s[x]
   if p!=".":
    if p.isupper()==w and p.upper()in ks:return 1
    break
   x+=d
 return 0
def EV(p,i):return (1if p.isupper()else-1)*(T[p.lower()][((i>>4)if p.isupper()else 7-(i>>4))*4+min(i&15,7-i&15)]if p.lower()in T else V[p.lower()])
def parse(fen):
 f=fen.split();s=["."]*128;i=112;ev=0
 for c in f[0]:
  if c.isdigit()or c=="/":i+=int(c)if c.isdigit()else-24
  else:s[i]=c;ev+=EV(c,i);i+=1
 cast=sum(1<<i for i,ch in enumerate("KQkq")if ch in f[2])
 ep=-1if f[3]=="-"else ord(f[3][0])-97+(int(f[3][1])-1)*16
 return[s,f[1],cast,ep,ev]
def mk(B,m):
 fr,to,pr=m;s=B[0][:];pc=s[fr];cast=B[2];ep=-1;ev=B[4];cq=to
 if pc.upper()=="P"and to==B[3]and fr%16!=to%16:cq=to-16if pc.isupper()else to+16
 cp=s[cq];ev-=EV(cp,cq);s[cq]="."
 ev-=EV(pc,fr);np=pr if pr else pc;s[to]=np;s[fr]=".";ev+=EV(np,to)
 if pc.upper()=="P"and abs(to-fr)==32:ep=(to+fr)//2
 if pc.upper()=="K"and abs(to-fr)==2:
  rf,rt=(fr+3,fr+1)if to>fr else(fr-4,fr-1);rp=s[rf];s[rt]=rp;s[rf]=".";ev+=EV(rp,rt)-EV(rp,rf)
 if pc.upper()=="K":cast&=~(3if pc=="K"else 12)
 cast&=~(RM.get(fr,0)|RM.get(to,0))
 return[s,"b"if B[1]=="w"else"w",cast,ep,ev]
def pm(o,i,t,w):o+=[(i,t,x.upper()if w else x)for x in"qrbn"]if t//16==(7if w else 0)else[(i,t,"")]
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
    if not t&136:
     if s[t]!="."and s[t].isupper()!=w:pm(out,i,t,w)
     elif t==B[3]:out.append((i,t,""))
  else:
   for ds,sl in(((ND,0),),((KD,0),),((BD,1),),((RD,1),),((KD,1),))["NKBRQ".index(u)]:
    for d in ds:
     t=i+d
     while not t&136:
      q=s[t]
      if q=="."or q.isupper()!=w:out.append((i,t,""))
      if q!="."or not sl:break
      t+=d
 h=116-112*w
 if s[h]==("K"if w else"k"):
  for sg,bt,rq,em,tr in((1,1if w else 4,h+3,(1,2),(0,1,2)),(-1,2if w else 8,h-4,(-1,-2,-3),(0,-1,-2))):
   if B[2]&bt and s[rq]==("R"if w else"r")and all(s[h+k]=="."for k in em)and not any(A(B,h+k,not w)for k in tr):out.append((h,h+2*sg,""))
 return out
def K(B):return "".join(B[0])+B[1]+chr(B[2])+str(B[3])
def S(B,d,a,b):
 N[0]+=1;w=B[1]=="w";s=B[0];ev=B[4]if w else-B[4]
 if N[0]>=N[1]or d<-8:return ev
 if d>0:
  tt=TT.get(K(B))
  if tt and tt[0]>=d:
   v=tt[1];f=tt[2]
   if f==0 or(f==1and v>=b):return v
 chk=A(B,s.index("K"if w else"k"),not w)
 if d<=0:
  if chk:ms=G(B,w);a=-2*MATE
  else:
   if ev>=b:return b
   a=max(a,ev);ms=[m for m in G(B,w)if s[m[1]]!="."or m[2]]
 else:ms=G(B,w)
 ms.sort(key=lambda m:(1<<18)+V[s[m[1]].lower()]*40 if s[m[1]]!="."else 0,reverse=True)
 best=-2*MATE
 for m in ms:
  B2=mk(B,m)
  if A(B2,B2[0].index("K"if w else"k"),not w):continue
  sc=-S(B2,d-1,-b,-a)
  if sc>best:best,bm=sc,m
  if sc>a:a=sc
  if a>=b:break
 if d<=0:return a
 if best==-2*MATE:return-MATE if chk else 0
 TT[K(B)]=(d,best,1if best>=b else 0,bm)
 return best
nm=lambda i:chr(97+i%16)+chr(49+i//16)
def C(fen):
 B=parse(fen);N[0]=0;bm=None
 for d in range(1,8):
  S(B,d,-2*MATE,2*MATE)
  if N[0]>=N[1]:break
  bm=TT[K(B)][3]
 bm=bm or TT[K(B)][3]
 return nm(bm[0])+nm(bm[1])+bm[2].lower()
U=os.getenv("MAKEFUN_ENV_URL")
def post(p,b):return json.load(ur.urlopen(U+p,json.dumps(b).encode()))
g={}
while g.get("status")!="done":
 g=post("/game",{})
 while g["status"]=="your_move":g=post("/move",{"game":g["game"],"move":C(g["fen"])})
