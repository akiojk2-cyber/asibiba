# あそびば 開発メモ（再開用）

2人対戦（iPadを中央に縦置き、上席は180°回転）のこども向けミニゲーム集。単一HTML・外部通信なし・PWAでオフライン動作。

## ファイル
- dev/asobiba_web.html : マスター（Artifact形式。doctype/head/bodyなし）。全16ゲーム+BGM
- dev/build_pwa.py     : マスター → pwa用index.html生成（CSP/manifest/SW登録を付与）、sw.jsのVERSION更新
- index.html / sw.js / manifest.webmanifest / icon-*.png : 公開物（GitHub Pages）

## 更新手順
1. dev/asobiba_web.html を編集
2. build_pwa.py を実行（例: python3 build_pwa.py asobiba-v7）→ pwa/index.html と pwa/sw.js を出力（スクリプト内のパスは作業環境に合わせて調整）
3. 出力の index.html / sw.js をリポジトリ直下へコピー → commit → push（Pages自動デプロイ）
4. sw.jsのVERSIONを必ず上げる（iPadは Wi-Fiで開いて閉じて再度開くと更新）
- 現在: v7（10えんはじき：盤面拡大・アウト/ゴールのランダムモード）。公開URL: https://akiojk2-cyber.github.io/asibiba/

## ゲーム（17）
オセロ / まるばつ / よんもくならべ / しんけいすいじゃく / どうぶつしょうぎ / しょうぎ（駒の動き表示・反則判定・千日手）/ はなふだ こいこい（役判定・SVG札）/ スピード（手札選択→場札タッチ）/ はやおし / つなひき / エアホッケー / ジャストタイム（10秒・7.77秒・ランダム）/ ピコピコ たいけつ / ほうせき さがし（紙コップ3〜5個・激ムズ）/ 10えん はじき / コイン ルーレット / ころころ ドロップ（ぷよぷよ風。iPad縦を左右に2分割、左は180°回転。連鎖・おじゃま・相殺・3〜5色。PY/pyXxx）

## 設計メモ
- 画面は position:fixed; inset:0。fitBoards()+ResizeObserverでBOARD_AR比に盤面幅を調整（iPadのタッチずれ対策）
- 上席は .side.top{transform:rotate(180deg)}。モーダルは上下2つ。神経衰弱の盤面・コップ台は手番側へ180°回転（.turned）
- 保存は localStorage 'asobiba-bgm' のみ。外部通信・入力欄なし。CSPは build_pwa.py で付与
- BGMはWebAudio（BGM/note()/sfx()）
- 将棋: kBoardMoves, kDropOK（二歩・打ち歩詰め）, kHasLegal
- 物理（10えんはじき）: hjFlick/hjStep。調整はnodeでシミュレーションして段差ごとに有効な強さ帯を確保
- テストはPlaywright(headless Chromium)。オフライン再読込（setOffline）を各版で確認

## 注意・既知
- Artifact形式のマスターを単体で開くにはdoctype+viewportのラッパーが必要
- ユーザー要望: 低学年にも分かるUI（ひらがな中心）、簡潔な修正指示
- 次の候補: QRコード、ポスター（別途Artifactで3案作成済み）、3年生向けにおとな向けゲームの分離
