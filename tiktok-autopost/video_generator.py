import logging
import os
import uuid

import fal_client
import requests

import config

logger = logging.getLogger(__name__)

os.environ["FAL_KEY"] = config.FAL_KEY


def _generate_clip(prompt: str) -> bytes:
    result = fal_client.run(
        "bytedance/seedance-2.0/fast/text-to-video",
        arguments={
            "prompt": prompt,
            "duration": "10",
            "aspect_ratio": "9:16",
            "resolution": "720p",
            "generate_audio": True,
        },
    )
    video_url = result["video"]["url"]
    resp = requests.get(video_url, timeout=120)
    resp.raise_for_status()
    return resp.content


def generate_clips(theme: dict, clip_count: int = 1) -> list[str]:
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    paths = []
    for i in range(clip_count):
        logger.info("動画 %d/%d 生成中...", i + 1, clip_count)
        video_bytes = _generate_clip(theme["prompt"])
        logger.info("動画生成完了 (%d bytes)", len(video_bytes))
        path = os.path.join(config.OUTPUT_DIR, f"clip_{uuid.uuid4().hex[:8]}.mp4")
        with open(path, "wb") as f:
            f.write(video_bytes)
        paths.append(path)
    return paths
