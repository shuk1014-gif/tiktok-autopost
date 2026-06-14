# セットアップ手順

## 1. 依存関係のインストール

```bash
pip install -r requirements.txt
# ffmpeg も必要
brew install ffmpeg        # Mac
apt install ffmpeg         # Ubuntu/Debian
```

## 2. Stability AI APIキー取得

1. https://platform.stability.ai/ にアクセス
2. サインアップ → API Keys → 新規キー作成
3. クレジット購入 (画像1枚 $0.065、動画1本 $0.20 / 3投稿/日 ≈ $3-4/日)

## 3. TikTok Developer 設定

1. https://developers.tiktok.com/ → ログイン
2. **My Apps** → **Create app**
3. App Name, Category, Description を入力して作成
4. **Products** タブ → **Content Posting API** を追加 (申請が必要)
5. **Manage app** → Client Key と Client Secret をコピー
6. **Login Kit** → Redirect URI に `http://localhost:8080/callback` を追加

> ⚠️ Content Posting API は申請承認が必要な場合があります。
> 審査中は Sandbox モードで `TIKTOK_PRIVACY=SELF_ONLY` でテスト可能です。

## 4. 環境変数の設定

```bash
cp .env.example .env
# .env をエディタで開いてキーを入力
```

## 5. TikTok 認証 (初回のみ)

```bash
python main.py auth
# ブラウザが開くので TikTok にログインして許可
# .tiktok_token.json が作成されます
```

## 6. テスト投稿 (1回だけ)

```bash
python main.py once
```

## 7. スケジューラー起動 (常駐)

```bash
python main.py start
# デフォルト: 07:00, 12:00, 20:00 に自動投稿
# POST_TIMES=09:00,15:00,21:00 で変更可
```

### バックグラウンド常駐 (Linux/Mac)

```bash
nohup python main.py start > /dev/null 2>&1 &
# または systemd service を設定
```

## BGM の追加 (任意)

`music/` フォルダに MP3 を入れると動画に自動でBGMが追加されます。

おすすめの無料音楽サイト:
- https://pixabay.com/music/
- https://freemusicarchive.org/
- YouTube Studio 音楽ライブラリ

## コスト目安

| 項目 | 単価 | 1日3投稿 (各4クリップ) |
|------|------|----------------------|
| 画像生成 | $0.065/枚 | $0.78 |
| 動画アニメーション | $0.20/本 | $2.40 |
| **合計** | | **≈ $3.18/日** |
