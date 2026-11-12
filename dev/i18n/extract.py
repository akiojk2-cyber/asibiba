import re,json,sys
src=open(sys.argv[2] if len(sys.argv)>2 else '/home/claude/asobiba_web.html').read()
JP=re.compile(r'[぀-ヿ一-鿿]')
# split html / script / style
parts=re.split(r'(<script[^>]*>.*?</script>|<style[^>]*>.*?</style>)',src,flags=re.S)
html=''.join(p for p in parts if not p.startswith('<script') and not p.startswith('<style'))
js='\n'.join(re.sub(r'^<script[^>]*>|</script>$','',p) for p in parts if p.startswith('<script'))
keys=[]
def norm(t):return re.sub(r'\s+',' ',t).strip()
def addfrags(h):
    # h: html fragment with ⟦n⟧ placeholders. split on tags
    for f in re.split(r'<[^>]+>',h):
        f=norm(f.replace('&nbsp;',' '))
        if JP.search(f):keys.append(f)
# static html text + attrs
addfrags(re.sub(r'<!--.*?-->','',html,flags=re.S))
for m in re.finditer(r'(?:aria-label|title|placeholder)="([^"]*)"',html):
    if JP.search(m.group(1)):keys.append(norm(m.group(1)))
# js lexer
lits=[];i=0;n=len(js)
def read_tpl(i):
    # i at char after `
    out='';ph=0
    while i<n:
        c=js[i]
        if c=='\\':out+=js[i:i+2];i+=2;continue
        if c=='`':return out,i+1
        if c=='$' and js[i+1]=='{':
            # find matching } with nested lexing
            j=i+2;depth=1;start=j
            while depth:
                c2=js[j]
                if c2 in '\'"':
                    s,j=read_str(j+1,c2);lits.append(s);continue
                if c2=='`':
                    s,j=read_tpl(j+1);lits.append(('T',s));continue
                if c2=='{':depth+=1
                elif c2=='}':depth-=1
                j+=1
            out+='⟦%d⟧'%ph;ph+=1;i=j;continue
        out+=c;i+=1
    return out,i
def read_str(i,q):
    out=''
    while js[i]!=q:
        if js[i]=='\\':out+=js[i+1];i+=2;continue
        out+=js[i];i+=1
    return out,i+1
prev=''
while i<n:
    c=js[i]
    if js.startswith('//',i) and prev not in ':\\':
        j=js.find('\n',i);i=j if j>=0 else n;continue
    if js.startswith('/*',i):i=js.find('*/',i)+2;continue
    if c in '\'"':
        s,i=read_str(i+1,c);lits.append(s);prev=c;continue
    if c=='`':
        s,i=read_tpl(i+1);lits.append(('T',s));continue
    # regex literal heuristic
    if c=='/' and re.match(r'[=(,:!&|?;{}\[]\s*$',js[max(0,i-3):i].rstrip()[-1:] or ';'):
        j=i+1
        while j<n and js[j]!='/' and js[j]!='\n':
            if js[j]=='\\':j+=1
            if js[j]=='[':
                while js[j]!=']':j+=1
            j+=1
        if j<n and js[j]=='/':i=j+1;continue
    if not c.isspace():prev=c
    i+=1
big=[]
for l in lits:
    tpl=isinstance(l,tuple)
    s=l[1] if tpl else l
    if not JP.search(s):continue
    if len(s)>300 and re.fullmatch(r'[぀-ヿ\s、,]+',s):big.append(len(s));continue
    addfrags(s)
seen=[];S=set()
for k in keys:
    if k not in S:S.add(k);seen.append(k)
json.dump(seen,open(sys.argv[1],'w'),ensure_ascii=False,indent=0)
print(len(seen),'keys; skipped big',big)
