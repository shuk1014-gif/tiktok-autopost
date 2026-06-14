import logging

import tweepy

import config

logger = logging.getLogger(__name__)

TIKTOK_URL = "https://www.tiktok.com/@animalvideo019"
FIXED_TAGS = "#癒し動画 #アニマル動画 #動物好き #もふもふ #AI動画"


def _make_tweet_text(theme: dict) -> str:
    title = theme.get("title", "")
    caption = theme.get("caption", "")
    text = f"{title}\n\n{caption}\n\n🎬 TikTokで動画公開中\n{TIKTOK_URL}\n\n{FIXED_TAGS}"
    return text[:280]


def _get_client():
    return tweepy.Client(
        consumer_key=config.X_API_KEY,
        consumer_secret=config.X_API_SECRET,
        access_token=config.X_ACCESS_TOKEN,
        access_token_secret=config.X_ACCESS_TOKEN_SECRET,
    )


def post_to_x(video_path: str, theme: dict) -> dict:
    client = _get_client()
    tweet_text = _make_tweet_text(theme)
    result = client.create_tweet(text=tweet_text)
    logger.info("X 投稿完了: tweet_id=%s", result.data["id"])
    return result.data
