import re
D='/tmp/claude-0/-home-claude/bb44f7ed-f9f2-508d-9f18-dca084f3f287/scratchpad/i18n/'
p='/home/claude/asobiba_web.html';s=open(p).read()
eng='/*I18N-START*/'+open(D+'engine_full.js').read()+'/*I18N-END*/\n'
if '/*I18N-START*/' in s:
  s=re.sub(r'/\*I18N-START\*/.*?/\*I18N-END\*/\n',lambda m:eng,s,flags=re.S)
else:
  i=s.rindex('</script>');s=s[:i]+eng+s[i:]
  R=[('<span class="hlp">${h[1]}</span>','<span class="hlp">${(HELP_L[LANG]&&HELP_L[LANG][sc.id])||h[1]}</span>'),
     ('<button class="bgm-btn" id="bgmMenu" onclick="bgmToggle()">🎵 おんがく：オン</button></div>',
      '<button class="bgm-btn" id="bgmMenu" onclick="bgmToggle()">🎵 おんがく：オン</button><button class="bgm-btn langbtn" id="langBtn" onclick="pickLang()">🌐 にほんご</button></div>'),
     ('<li>🎵 で おんがくの オン・オフが きりかえられるよ。</li>','<li>🎵 で おんがくの オン・オフが きりかえられるよ。🌐 で ことば（English など）を えらべるよ。</li>'),
     ('端末に残るのは、アプリ本体のファイルと「おんがくのオン・オフ」の設定だけです。','端末に残るのは、アプリ本体のファイルと「おんがくのオン・オフ」「ことば（言語）」の設定だけです。'),
     ('.menubtns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}','.menubtns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}\n.mbtns.langrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}.mbtns.langrow .mbtn{margin:0}'),
  ]
  for a,b in R:
    assert s.count(a)==1,a;s=s.replace(a,b)
open(p,'w').write(s)
