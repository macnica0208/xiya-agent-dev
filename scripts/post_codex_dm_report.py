"""Send an engineering report DM through the configured Codex/test bot.

This is intentionally separate from Xiya's in-character Discord channel.
Secrets and recipient IDs are read from env/runtime_data, not committed docs.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = PLUGIN_ROOT / "runtime_data"
TEST_SENDER_CONFIG_PATH = RUNTIME_ROOT / "discord_test_sender_config.json"
REPORT_CONFIG_PATH = RUNTIME_ROOT / "codex_report_dm_config.json"


class DiscordHttpError(RuntimeError):
    def __init__(self, message: str, *, status: int = 0, body_preview: str = "") -> None:
        super().__init__(message)
        self.status = status
        self.body_preview = body_preview


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return dict(data) if isinstance(data, dict) else {}


def _save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_token() -> tuple[str, str]:
    for env_name in ("XIYA_CODEX_REPORT_DISCORD_TOKEN", "XIYA_V2_TEST_DISCORD_TOKEN", "XIYA_TEST_DISCORD_TOKEN"):
        token = str(os.environ.get(env_name) or "").strip()
        if token:
            return token, f"env:{env_name}"
    config = _load_json(TEST_SENDER_CONFIG_PATH)
    token = str(config.get("token") or "").strip()
    return token, str(TEST_SENDER_CONFIG_PATH) if token else ""


def _request_json(token: str, method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "codex-report-dm/0.1",
    }
    if payload is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request("https://discord.com/api/v10" + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise DiscordHttpError("discord_http_error", status=exc.code, body_preview=body[:500]) from exc
    return json.loads(raw.decode("utf-8")) if raw else {}


def _multipart_body(*, boundary: str, payload: dict[str, Any], file_path: Path) -> bytes:
    file_bytes = file_path.read_bytes()
    parts = [
        f"--{boundary}\r\n".encode("utf-8"),
        b'Content-Disposition: form-data; name="payload_json"\r\n',
        b"Content-Type: application/json\r\n\r\n",
        json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        b"\r\n",
        f"--{boundary}\r\n".encode("utf-8"),
        f'Content-Disposition: form-data; name="files[0]"; filename="{file_path.name}"\r\n'.encode("utf-8"),
        b"Content-Type: application/octet-stream\r\n\r\n",
        file_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode("utf-8"),
    ]
    return b"".join(parts)


def _request_message_with_file(token: str, channel_id: str, content: str, file_path: Path) -> Any:
    boundary = f"codex-report-{int(time.time() * 1000)}"
    payload = {"content": content, "allowed_mentions": {"parse": []}}
    body = _multipart_body(boundary=boundary, payload=payload, file_path=file_path)
    headers = {
        "Authorization": f"Bot {token}",
        "User-Agent": "codex-report-dm/0.1",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    request = urllib.request.Request(
        f"https://discord.com/api/v10/channels/{channel_id}/messages",
        data=body,
        method="POST",
        headers=headers,
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        body_preview = exc.read().decode("utf-8", errors="replace")
        raise DiscordHttpError("discord_http_error", status=exc.code, body_preview=body_preview[:500]) from exc
    return json.loads(raw.decode("utf-8")) if raw else {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Post a Codex engineering report DM.")
    parser.add_argument("--content", required=True)
    parser.add_argument("--recipient-id", default="")
    parser.add_argument("--file", default="")
    parser.add_argument("--refresh-dm", action="store_true")
    args = parser.parse_args()

    token, token_source = _load_token()
    report_config = _load_json(REPORT_CONFIG_PATH)
    recipient_id = str(args.recipient_id or os.environ.get("XIYA_CODEX_REPORT_USER_ID") or report_config.get("recipient_id") or "").strip()
    dm_channel_id = str(report_config.get("dm_channel_id") or "").strip()
    result: dict[str, Any] = {
        "ok": False,
        "token_source": "***configured***" if token else "",
        "recipient_id": recipient_id,
        "dm_channel_id": dm_channel_id,
        "message_id": "",
        "file_path": str(args.file or ""),
    }
    if not token:
        result["error"] = "missing_codex_report_token"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    if not recipient_id:
        result["error"] = "missing_recipient_id"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    try:
        if args.refresh_dm or not dm_channel_id:
            dm = _request_json(token, "POST", "/users/@me/channels", {"recipient_id": recipient_id})
            dm_channel_id = str(dict(dm).get("id") or "")
            report_config["recipient_id"] = recipient_id
            report_config["dm_channel_id"] = dm_channel_id
            _save_json(REPORT_CONFIG_PATH, report_config)
        file_path = Path(args.file).expanduser() if args.file else None
        if file_path:
            if not file_path.exists() or not file_path.is_file():
                raise FileNotFoundError(str(file_path))
            message = _request_message_with_file(token, dm_channel_id, str(args.content or ""), file_path)
        else:
            message = _request_json(
                token,
                "POST",
                f"/channels/{dm_channel_id}/messages",
                {"content": str(args.content or ""), "allowed_mentions": {"parse": []}},
            )
        result["ok"] = True
        result["dm_channel_id"] = dm_channel_id
        result["message_id"] = str(dict(message).get("id") or "")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except DiscordHttpError as exc:
        result["error"] = str(exc)
        result["status"] = exc.status
        result["body_preview"] = exc.body_preview
    except Exception as exc:  # noqa: BLE001
        result["error"] = exc.__class__.__name__
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

