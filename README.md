# Hello World SDD デモ（モノレポ / BE + FE）

仕様(spec) → 振る舞い(Gherkin) → 実装 → 検証 の流れを、
backend / frontend に分けて体験する最小セット。
Gherkinは「設計・AIへの指示書」。テストは実ツール（pytest / Playwright）で書く。

## ディレクトリ構成
```
greeting_demo/
├── specs/                      … 仕様（Why/What）。BE/FE共通。人間が決める。
│   ├── spec1_greeting.md
│   └── spec2_history.md
├── features/                   … 振る舞い(Gherkin)。AIへの指示書 / チームの合意。
│   ├── backend_greeting.feature   … BE：APIの振る舞い
│   └── frontend_greeting.feature  … FE：画面の振る舞い
└── apps/
    ├── backend/                … バックエンド（Flask API）
    │   ├── greeting.py            … ロジック本体（仕様の真実はここに一本化）
    │   ├── app.py                 … APIサーバー（/greet, /history）
    │   └── tests/
    │       └── test_greeting.py   … ロジックの検証（pytest）
    └── frontend/               … フロントエンド（APIを呼ぶ画面）
        ├── index.html             … 画面。fetchでBE APIを叩く
        └── tests/
            └── test_greeting_ui.py … 画面の検証（Playwright・E2E）
```

## 層の対応
| 層 | Gherkin                    | 実装                  | テスト                  | 関心事        |
|----|----------------------------|-----------------------|-------------------------|--------------|
| BE | backend_greeting.feature   | apps/backend/         | pytest（ロジック）      | 値が「返る」  |
| FE | frontend_greeting.feature  | apps/frontend/        | Playwright（画面通し）  | 画面に「表示」|

ロジックの真実はBEに一本化。FEはAPIを呼ぶだけ。
FE用Gherkinは BE用の書き直しではなく「追加」。両方が並存する。

---

## セットアップ（最初の1回）
```
python -m pip install flask flask-cors pytest playwright pytest-playwright
python -m playwright install chromium
```
（Windows では `python3` ではなく `python` を使う。`python3` は Microsoft Store のダミーで動かないため）

---

## 起動方法

### 1. バックエンド（API）を起動する
```
cd apps/backend
python app.py
```
→ http://localhost:5001 でAPIが起動する。
   このターミナルは起動したまま（サーバーが動き続ける）にする。

動作確認（別ターミナルで）。1行で書くのが確実:
```
curl -X POST http://localhost:5001/greet -H "Content-Type: application/json" -d "{\"number\":2}"
# => {"message":"こんにちは、世界！"}

curl http://localhost:5001/history
# => {"history":["こんにちは、世界！"]}
```
※ PowerShell では `curl` が別コマンド(Invoke-WebRequest)に化けることがある。
  その場合は `curl.exe ...` と明示するか、動作確認はブラウザで画面を開いて行う。

### 2. フロントエンド（画面）を起動する
BEを起動したまま、別のターミナルを開いて:
```
cd apps/frontend
python -m http.server 8000
```
→ ブラウザで http://localhost:8000/index.html を開く。
   日本語/英語ボタンを押すと、BE APIを呼んであいさつと履歴が表示される。

※ BEが起動していないと、画面のボタンを押しても何も表示されない
  （FEはBEのAPIに依存しているため）。

---

## 検証（テスト）の実行

### バックエンドのテスト（pytest・速い）
```
cd apps/backend
python -m pytest tests/ -v
```
ロジックを直接検証する。APIサーバーの起動は不要。

### フロントエンドのテスト（Playwright・E2E）
```
cd apps/frontend
python -m pytest tests/ -v
```
テストが内部で自動的にBE APIと画面サーバーを起動し、
ブラウザでボタンを操作して、表示を検証する。
（事前に手動でサーバーを起動しておく必要はない）

---

## うまく動かないとき（ポート競合）
テストを連続で回すと、前のプロセスが残ってポート5001/8000が
塞がる（Address already in use）ことがある。残プロセスを止める:

Windows:
```
netstat -ano | findstr :5001
taskkill /PID <表示されたPID> /F
```
Mac / Linux:
```
lsof -ti:5001 | xargs kill -9
```

---

## 試すと面白いこと（番人の働きを見る）
- apps/backend/greeting.py の append を insert(0) に変える
  → BEテスト（pytest）の履歴順テストが FAILED
- apps/frontend/index.html の history.forEach の前で配列を reverse する等
  → FEテスト（Playwright）が FAILED
各層の番人が、それぞれの層のバグを捕まえる。
