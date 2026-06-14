import json
import logging
import os
import secrets
import time
import urllib.parse

import requests

import config

logger = logging.getLogger(__name__)

AUTH_BASE = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
SCOPES = "video.upload"


def run_oauth_flow() -> dict:
    state = secrets.token_urlsafe(16)
    params = {
        "client_key": config.TIKTOK_CLIENT_KEY,
        "response_type": "code",
        "scope": SCOPES,
        "redirect_uri": config.TIKTOK_REDIRECT_URI,
        "state": state,
    }
    auth_url = AUTH_BASE + "?" + urllib.parse.urlencode(params)

    print("\n" + "=" * 60)
    print("以下のURLをブラウザで開いてTikTokにログインしてください:")
    print(auth_url)
    print("=" * 60)
    print("\nログイン後、ページに表示された「認証コード」を貼り付けてください:")

    code = input("認証コード: ").strip()
    if not code:
        raise ValueError("認証コードが入力されていません")

    resp = requests.post(
        TOKEN_URL,
        data={
            "client_key": config.TIKTOK_CLIENT_KEY,
            "client_secret": config.TIKTOK_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": config.TIKTOK_REDIRECT_URI,
        },
        timeout=30,
    )
    resp.raise_for_status()
    token_data = resp.json()
    token_data["obtained_at"] = int(time.time())
    _save_token(token_data)
    logger.info("OAuth 完了、トークン保存済み")
    return token_data


def _save_token(data: dict):
    with open(config.TOKEN_FILE, "w") as f:
        json.dump(data, f)


def _load_token() -> dict | None:
    if not os.path.exists(config.TOKEN_FILE):
        return None
    with open(config.TOKEN_FILE) as f:
        return json.load(f)


def _refresh_token(token_data: dict) -> dict:
    resp = requests.post(
        TOKEN_URL,
        data={
            "client_key": config.TIKTOK_CLIENT_KEY,
            "client_secret": config.TIKTOK_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"],
        },
        timeout=30,
    )
    resp.raise_for_status()
    new_data = resp.json()
    new_data["obtained_at"] = int(time.time())
    _save_token(new_data)
    logger.info("トークンをリフレッシュしました")
    return new_data


def get_valid_token() -> str:
    token_data = _load_token()
    if token_data is None:
        token_data = run_oauth_flow()

    obtained_at = token_data.get("obtained_at", 0)
    expires_in = token_data.get("expires_in", 86400)
    if int(time.time()) > obtained_at + expires_in - 300:
        token_data = _refresh_token(token_data)

    return token_data["access_token"]
