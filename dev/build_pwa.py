import re,sys
ver=sys.argv[1]
body=open('asobiba_web.html',encoding='utf8').read()
te=body.index('</title>')+len('</title>')
meta='''
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="あそびば">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="theme-color" content="#fff6e0">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="icon-180.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}</style>
'''
b=body[:te]+meta+body[te:]
b=b.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
mse=b.index('</style>',b.index('/* 縦向きiPad'))+len('</style>')
head='''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; manifest-src 'self'; worker-src 'self'; media-src 'none'; object-src 'none'; frame-src 'none'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer">
'''
b=head+b[:mse]+'\n</head>\n<body>'+b[mse:].rstrip()+'''
<script>
if('serviceWorker' in navigator){window.addEventListener('load',()=>{navigator.serviceWorker.register('sw.js',{scope:'./'}).catch(()=>{});});}
</script>
</body>
</html>
'''
open('pwa/index.html','w',encoding='utf8').write(b)
w=open('pwa/sw.js',encoding='utf8').read()
w=re.sub(r"const VERSION='[^']+';",f"const VERSION='{ver}';",w)
open('pwa/sw.js','w',encoding='utf8').write(w)
