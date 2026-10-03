# gcp — GCP Deploy TUI

A `curses`-based terminal UI for deploying the proxy stack to GCP:
interactive menus, spinners, and client-link generation.

## Run

```bash
pip install requests
python3 gcp.py
```

(Linux/macOS terminal with curses support.)

## Configuration

| Env var | Purpose |
|---|---|
| `PRVTSPYYY_PASSWORD` | SSH password (otherwise you are prompted securely) |

The WebSocket path defaults to `/prvtspyyy404` (see `WS_PATH` in `gcp.py`).

## Files

| File | Purpose |
|---|---|
| `gcp.py` | The TUI app (stdlib + `requests`) |

## Security notes

- The password is never stored — pass it via env var or the secure prompt.
- Keep generated client links private.
