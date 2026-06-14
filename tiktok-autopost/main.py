import argparse
import logging
import os
import sys
import time

import schedule

import config
from animal_prompts import get_daily_themes, get_random_theme
from video_editor import edit_for_tiktok
from video_generator import generate_clips
from tiktok_client import post_video
from x_client import post_to_x

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("main")


def _validate_env():
    missing = []
    if not config.FAL_KEY:
        missing.append("FAL_KEY")
    if not config.TIKTOK_CLIENT_KEY:
        missing.append("TIKTOK_CLIENT_KEY")
    if not config.TIKTOK_CLIENT_SECRET:
        missing.append("TIKTOK_CLIENT_SECRET")
    if missing:
        logger.error("環境変数が設定されていません: %s", ", ".join(missing))
        sys.exit(1)


def run_post_job(theme: dict | None = None):
    if theme is None:
        theme = get_random_theme()

    logger.info("=== 投稿開始: %s ===", theme.get("title", ""))
    clip_paths = []
    video_path = None

    try:
        clip_paths = generate_clips(theme, clip_count=2)
        video_path = edit_for_tiktok(clip_paths, theme)
        result = post_video(video_path, theme)
        logger.info("=== TikTok 投稿完了 === %s", result)

        try:
            x_result = post_to_x(video_path, theme)
            logger.info("=== X 投稿完了 === %s", x_result)
        except Exception as e:
            logger.error("X 投稿失敗（TikTok は成功済み）: %s", e)

    except Exception as e:
        logger.exception("投稿失敗: %s", e)

    finally:
        if video_path and os.path.exists(video_path):
            try:
                os.remove(video_path)
            except OSError:
                pass


def run_scheduler():
    _validate_env()
    logger.info("スケジューラー起動: 投稿時刻 = %s", config.POST_TIMES)

    for post_time in config.POST_TIMES:
        schedule.every().day.at(post_time.strip(), "Asia/Tokyo").do(run_post_job)

    logger.info("待機中... (Ctrl+C で停止)")
    while True:
        schedule.run_pending()
        time.sleep(30)


def run_once():
    _validate_env()
    theme = get_random_theme()
    logger.info("テスト投稿: %s", theme.get("title", ""))
    run_post_job(theme)


def run_auth_only():
    from tiktok_auth import run_oauth_flow
    token_data = run_oauth_flow()
    print(f"\nアクセストークン取得成功!")
    print(f"有効期限: {token_data.get('expires_in', '?')} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok 動物動画自動投稿ツール")
    parser.add_argument(
        "command",
        nargs="?",
        default="start",
        choices=["start", "once", "auth"],
        help="start=スケジューラー起動 / once=1回だけ投稿 / auth=TikTok認証のみ",
    )
    args = parser.parse_args()

    if args.command == "start":
        run_scheduler()
    elif args.command == "once":
        run_once()
    elif args.command == "auth":
        run_auth_only()
