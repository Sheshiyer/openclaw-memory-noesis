#!/usr/bin/env python3
import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request


class CloudflareKVError(Exception):
    pass


class CloudflareKVClient:
    def __init__(self, account_id: str, api_token: str, namespace_id: str | None = None):
        self.account_id = account_id
        self.api_token = api_token
        self.namespace_id = namespace_id

    def _request(self, method: str, path: str, *, body: bytes | None = None, headers: dict | None = None) -> bytes:
        url = f"https://api.cloudflare.com/client/v4{path}"
        req_headers = {
            "Authorization": f"Bearer {self.api_token}",
        }
        if headers:
            req_headers.update(headers)
        req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            raw = e.read()
            try:
                payload = json.loads(raw.decode("utf-8"))
                raise CloudflareKVError(payload.get("errors") or payload.get("messages") or payload) from None
            except Exception:
                raise CloudflareKVError(raw.decode("utf-8", errors="replace")) from None
        except urllib.error.URLError as e:
            raise CloudflareKVError(str(e)) from None

    def list_namespaces(self) -> list[dict]:
        raw = self._request("GET", f"/accounts/{self.account_id}/storage/kv/namespaces")
        payload = json.loads(raw.decode("utf-8"))
        if not payload.get("success"):
            raise CloudflareKVError(payload.get("errors") or payload)
        return payload.get("result") or []

    def get_value(self, key: str, namespace_id: str | None = None) -> bytes:
        ns = namespace_id or self.namespace_id
        if not ns:
            raise CloudflareKVError("namespace_id is required")
        key_enc = urllib.parse.quote(key, safe="")
        return self._request(
            "GET",
            f"/accounts/{self.account_id}/storage/kv/namespaces/{ns}/values/{key_enc}",
        )

    def put_value(self, key: str, value: bytes, namespace_id: str | None = None) -> None:
        ns = namespace_id or self.namespace_id
        if not ns:
            raise CloudflareKVError("namespace_id is required")
        key_enc = urllib.parse.quote(key, safe="")
        raw = self._request(
            "PUT",
            f"/accounts/{self.account_id}/storage/kv/namespaces/{ns}/values/{key_enc}",
            body=value,
            headers={"Content-Type": "application/octet-stream"},
        )
        payload = json.loads(raw.decode("utf-8"))
        if not payload.get("success"):
            raise CloudflareKVError(payload.get("errors") or payload)

    def delete_value(self, key: str, namespace_id: str | None = None) -> None:
        ns = namespace_id or self.namespace_id
        if not ns:
            raise CloudflareKVError("namespace_id is required")
        key_enc = urllib.parse.quote(key, safe="")
        raw = self._request(
            "DELETE",
            f"/accounts/{self.account_id}/storage/kv/namespaces/{ns}/values/{key_enc}",
        )
        payload = json.loads(raw.decode("utf-8"))
        if not payload.get("success"):
            raise CloudflareKVError(payload.get("errors") or payload)


def _load_env_kv_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    if not isinstance(cfg, dict):
        raise ValueError("env-kv config must be a JSON object")
    return cfg


def _write_env_file_from_config(config_path: str, out_path: str) -> None:
    cfg = _load_env_kv_config(config_path)
    account_id = cfg.get("account_id") or os.getenv("CLOUDFLARE_ACCOUNT_ID")
    namespace_id = cfg.get("namespace_id") or os.getenv("CLOUDFLARE_KV_NAMESPACE_ID")
    token_env_var = cfg.get("token_env_var") or "CLOUDFLARE_API_TOKEN"
    api_token = os.getenv(token_env_var)
    keys = cfg.get("keys") or {}

    if not account_id:
        raise ValueError("Missing account_id (config.account_id or CLOUDFLARE_ACCOUNT_ID)")
    if not namespace_id:
        raise ValueError("Missing namespace_id (config.namespace_id or CLOUDFLARE_KV_NAMESPACE_ID)")
    if not api_token:
        raise ValueError(f"Missing API token env var: {token_env_var}")
    if not isinstance(keys, dict) or not keys:
        raise ValueError("Missing keys map in config (e.g., {\"ANTHROPIC_API_KEY\": \"anthropic_api_key\"})")

    client = CloudflareKVClient(account_id=account_id, api_token=api_token, namespace_id=namespace_id)

    lines: list[str] = []
    for env_name, kv_key in keys.items():
        if not isinstance(env_name, str) or not isinstance(kv_key, str):
            raise ValueError("keys map must be string-to-string")
        value_bytes = client.get_value(kv_key)
        value = value_bytes.decode("utf-8", errors="strict")
        escaped = value.replace("\\", "\\\\").replace("'", "'\"'\"'")
        lines.append(f"{env_name}='{escaped}'")

    tmp_dir = os.path.dirname(out_path) or "."
    os.makedirs(tmp_dir, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".env-kv.", dir=tmp_dir, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            f.write("\n")
        os.replace(tmp_path, out_path)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(prog="cloudflare_kv.py")
    parser.add_argument("--account-id", default=os.getenv("CLOUDFLARE_ACCOUNT_ID"))
    parser.add_argument("--namespace-id", default=os.getenv("CLOUDFLARE_KV_NAMESPACE_ID"))
    parser.add_argument("--token-env", default="CLOUDFLARE_API_TOKEN")

    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-namespaces")

    get_p = sub.add_parser("get")
    get_p.add_argument("key")

    put_p = sub.add_parser("put")
    put_p.add_argument("key")
    put_p.add_argument("value")

    del_p = sub.add_parser("delete")
    del_p.add_argument("key")

    env_p = sub.add_parser("write-env-file")
    env_p.add_argument("--config", required=True)
    env_p.add_argument("--out", required=True)

    args = parser.parse_args()

    if args.cmd == "write-env-file":
        _write_env_file_from_config(args.config, args.out)
        return 0

    account_id = args.account_id
    namespace_id = args.namespace_id
    api_token = os.getenv(args.token_env)

    if not account_id:
        raise CloudflareKVError("Missing CLOUDFLARE_ACCOUNT_ID (or --account-id)")
    if not api_token:
        raise CloudflareKVError(f"Missing {args.token_env} (API token env var)")

    client = CloudflareKVClient(account_id=account_id, api_token=api_token, namespace_id=namespace_id)

    if args.cmd == "list-namespaces":
        print(json.dumps(client.list_namespaces(), indent=2))
        return 0

    if not namespace_id:
        raise CloudflareKVError("Missing CLOUDFLARE_KV_NAMESPACE_ID (or --namespace-id)")

    if args.cmd == "get":
        sys.stdout.buffer.write(client.get_value(args.key))
        return 0
    if args.cmd == "put":
        client.put_value(args.key, args.value.encode("utf-8"))
        return 0
    if args.cmd == "delete":
        client.delete_value(args.key)
        return 0

    raise CloudflareKVError("Unknown command")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CloudflareKVError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        raise SystemExit(1)
