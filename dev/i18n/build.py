import json,re,sys
D='/tmp/claude-0/-home-claude/bb44f7ed-f9f2-508d-9f18-dca084f3f287/scratchpad/i18n/'
keys=dict(json.load(open(D+'keys3.json')))
L=['en','uk','zh','ko','es','pt'];I={l:{} for l in L};bad=[]
for f in ['t1','t2','t3','t4','t5','t6']:
  for line in open(D+f+'.txt'):
    line=line.rstrip('\n')
    if not line.strip():continue
    p=line.split('¦')
    if len(p)!=7:bad.append(('cols',line));continue
    i=int(p[0]);k=keys.get(i)
    if k is None:bad.append(('nokey',i));continue
    need=set(re.findall(r'\{\d+\}',k))
    for l,v in zip(L,p[1:]):
      if v=='' :continue
      if v=='∅':v=''
      if set(re.findall(r'\{\d+\}',v))!=need:bad.append(('ph',i,l,v))
      I[l][k]=v
# special
for l in ['en','uk','es','pt']:I[l]['こ']=''
missing=[k for i,k in keys.items() if k not in I['en'] and len(k)>1]
help_src='const HELP_L={\n'+''.join(open(D+'help_%s.js'%l).read() for l in L)+'};\n'
js=open(D+'engine.js').read().replace('/*@@I18N@@*/','const I18N='+json.dumps(I,ensure_ascii=False)+';\n'+help_src+open(D+'howto.js').read())
open(D+'engine_full.js','w').write(js)
print('bad',bad[:20],len(bad));print('missing en',missing)
print({l:len(I[l]) for l in L})
