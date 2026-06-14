import logging
import math
import os
import time

import requests

import config
from tiktok_auth import get_valid_token

logger = logging.getLogger(__name__)

API_BASE = "https://open.tiktokapis.com"
CHUNK_SIZE = 10 * 1024 * 1024


def _api_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8",
    }


def _init_upload(token: str, file_size: int, title: str) -> tuple[str, str]:
    total_chunks = math.ceil(file_size / CHUNK_SIZE)
    chunk_size = min(CHUNK_SIZE, file_size)

    payload = {
        "post_info": {
            "title": title[:2200],
            "privacy_level": config.TIKTOK_PRIVACY,
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000,
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": chunk_size,
            "total_chunk_count": total_chunks,
        },
    }
    resp = requests.post(
        f"{API_BASE}/v2/post/publish/inbox/video/init/",
        headers=_api_headers(token),
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()["data"]
    return data["publish_id"], data["upload_url"]


def _upload_chunks(upload_url: str, video_path: str):
    file_size = os.path.getsize(video_path)
    total_chunks = math.ceil(file_size / CHUNK_SIZE)

    with open(video_path, "rb") as f:
        for i in range(total_chunks):
            chunk = f.read(CHUNK_SIZE)
            start = i * CHUNK_SIZE
            end = start + len(chunk) - 1
            headers = {
                "Content-Range": f"bytes {start}-{end}/{file_size}",
                "Content-Type": "video/mp4",
            }
            resp = requests.put(upload_url, headers=headers, data=chunk, timeout=120)
            resp.raise_for_status()
            logger.info("チャンク %d/%d アップロード完了", i + 1, total_chunks)


def _wait_for_publish(token: str, publish_id: str) -> dict:
    for _ in range(60):
        time.sleep(10)
        resp = requests.post(
            f"{API_BASE}/v2/post/publish/status/fetch/",
            headers=_api_headers(token),
            json={"publish_id": publish_id},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()["data"]
        status = data.get("status")
        logger.info("投稿ステータス: %s", status)
        if status in ("PUBLISH_COMPLETE", "SUCCESS", "SEND_TO_USER_INBOX"):
            return data
        if status in ("FAILED", "ERROR"):
            raise RuntimeError(f"TikTok 投稿失敗: {data}")
    raise TimeoutError("投稿ステータス確認タイムアウト")


def post_video(video_path: str, theme: dict) -> dict:
    token = get_valid_token()
    file_size = os.path.getsize(video_path)
    title = theme.get("title", "")
    caption = theme.get("caption", "")
    fixed_tags = "#癒し動画\n#アニマル動画\n#動物好き\n#もふもふ\n#AI動画"
    description = f"{title}\n\n{caption}\n\n{fixed_tags}"

    logger.info("アップロード初期化 (%d bytes)", file_size)
    publish_id, upload_url = _init_upload(token, file_size, description)

    logger.info("動画チャンクアップロード中...")
    _upload_chunks(upload_url, video_path)

    logger.info("投稿完了を待機中 (publish_id=%s)", publish_id)
    result = _wait_for_publish(token, publish_id)
    logger.info("TikTok 投稿成功: %s", result)
    return result
