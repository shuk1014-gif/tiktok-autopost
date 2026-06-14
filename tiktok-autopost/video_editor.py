import glob
import logging
import os
import random
import uuid

from moviepy import AudioFileClip, CompositeVideoClip, TextClip, VideoFileClip, concatenate_videoclips

import config

logger = logging.getLogger(__name__)

TARGET_W = config.VIDEO_WIDTH
TARGET_H = config.VIDEO_HEIGHT


def _add_caption(clip, text: str):
    try:
        txt = TextClip(
            font="Arial-Bold",
            text=text,
            font_size=55,
            color="white",
            stroke_color="black",
            stroke_width=3,
            method="caption",
            size=(TARGET_W - 80, None),
        )
        txt = txt.with_position(("center", TARGET_H - txt.h - 120)).with_duration(clip.duration)
        return CompositeVideoClip([clip, txt], size=(TARGET_W, TARGET_H))
    except Exception as e:
        logger.warning("テキスト追加スキップ: %s", e)
        return clip


def _pick_music() -> str | None:
    files = []
    for pattern in ["*.mp3", "*.m4a", "*.wav"]:
        files.extend(glob.glob(os.path.join(config.MUSIC_DIR, pattern)))
    return random.choice(files) if files else None


def edit_for_tiktok(clip_paths: list[str], theme: dict) -> str:
    clips = [VideoFileClip(p) for p in clip_paths]
    combined = concatenate_videoclips(clips, method="compose") if len(clips) > 1 else clips[0]

    combined = _add_caption(combined, theme.get("caption", ""))

    music_path = _pick_music()
    if music_path:
        audio = AudioFileClip(music_path).subclipped(0, combined.duration).audio_fadeout(2)
        combined = combined.with_audio(audio)

    out_path = os.path.join(config.OUTPUT_DIR, f"tiktok_{uuid.uuid4().hex[:8]}.mp4")
    combined.write_videofile(
        out_path,
        codec="libx264",
        audio_codec="aac",
        fps=30,
        preset="fast",
        logger=None,
    )

    for c in clips:
        c.close()
    for p in clip_paths:
        try:
            os.remove(p)
        except OSError:
            pass

    logger.info("編集完了: %s", out_path)
    return out_path
