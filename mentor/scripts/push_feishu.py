#!/usr/bin/env python3
"""把一段文本推送到飞书自定义机器人。

用法:
    python push_feishu.py --text "内容"
    python push_feishu.py --file path/to/reflection.md
    echo "内容" | python push_feishu.py

配置从 knowledge/config.json 的 feishu 段读取 (webhook_url, secret)。
支持飞书「签名校验」: 如果 config 里填了 secret 就自动加签。
仅用 Python 标准库, 无需 pip 安装。
"""
import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "knowledge" / "config.json"


def load_feishu_config(config_path: Path) -> dict:
    if not config_path.exists():
        sys.exit(f"[push_feishu] 找不到配置文件: {config_path}")
    data = json.loads(config_path.read_text(encoding="utf-8"))
    feishu = data.get("feishu", {})
    if not feishu.get("webhook_url"):
        sys.exit(
            "[push_feishu] 还没配置飞书 webhook_url。\n"
            f"请编辑 {config_path}, 把飞书自定义机器人的 Webhook 地址填进 feishu.webhook_url。"
        )
    return feishu


def gen_sign(secret: str, timestamp: int) -> str:
    string_to_sign = f"{timestamp}\n{secret}"
    digest = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    return base64.b64encode(digest).decode("utf-8")


def build_payload(text: str, secret: str) -> dict:
    payload = {"msg_type": "text", "content": {"text": text}}
    if secret:
        ts = int(time.time())
        payload["timestamp"] = str(ts)
        payload["sign"] = gen_sign(secret, ts)
    return payload


def send(webhook_url: str, payload: dict) -> None:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url, data=body, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        sys.exit(f"[push_feishu] 请求失败: {e}")
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(f"[push_feishu] 飞书返回非 JSON: {raw}")
    # 飞书成功时返回 {"code":0,...} 或 {"StatusCode":0,...}
    code = result.get("code", result.get("StatusCode", 0))
    if code != 0:
        sys.exit(f"[push_feishu] 飞书拒绝了消息: {raw}")
    print("[push_feishu] 推送成功 ✅")


def main() -> None:
    parser = argparse.ArgumentParser(description="推送文本到飞书自定义机器人")
    parser.add_argument("--text", help="直接传入要推送的文本")
    parser.add_argument("--file", help="从文件读取要推送的文本")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="config.json 路径")
    args = parser.parse_args()

    if args.text is not None:
        text = args.text
    elif args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    text = text.strip()
    if not text:
        sys.exit("[push_feishu] 没有要推送的内容。")

    feishu = load_feishu_config(Path(args.config))
    payload = build_payload(text, feishu.get("secret", ""))
    send(feishu["webhook_url"], payload)


if __name__ == "__main__":
    main()
