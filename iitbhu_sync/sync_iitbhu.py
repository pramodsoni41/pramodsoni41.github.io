"""
IITBHU Sync Launcher
Flow:
  1. Read URL from url_home.txt (same folder as exe)
  2. If login URL  → show credential dialog (pre-filled), POST login
  3. After login   → url_home.txt switches to keepalive URL automatically
  4. Ping keepalive URL every KEEPALIVE_INTERVAL seconds to stay connected
  5. Launch FreeFileSync
  6. Sit in system tray; right-click → Quit to exit
"""

import sys
import os
import time
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox

import keyring
import requests
from PIL import Image, ImageDraw
import pystray

# ── Config ────────────────────────────────────────────────────────────────────
SERVICE_NAME       = "IITBHU_Sync"
FFS_CONFIG         = r"D:\SyncSettings_IITBHU.ffs_gui"
FFS_EXE            = r"C:\Program Files\FreeFileSync\FreeFileSync.exe"
KEEPALIVE_INTERVAL = 180        # seconds between keepalive pings (3 min)
FIELD_USER         = "username"  # adjust if login form uses different names
FIELD_PASS         = "password"
# ──────────────────────────────────────────────────────────────────────────────


def _exe_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def read_url() -> str:
    path = os.path.join(_exe_dir(), "url_home.txt")
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        messagebox.showerror("Missing file", f"url_home.txt not found next to exe:\n{path}")
        sys.exit(1)


# ── Credentials ───────────────────────────────────────────────────────────────

def load_credentials():
    u = keyring.get_password(SERVICE_NAME, "username")
    p = keyring.get_password(SERVICE_NAME, "password") if u else None
    return u or "", p or ""


def save_credentials(u, p):
    keyring.set_password(SERVICE_NAME, "username", u)
    keyring.set_password(SERVICE_NAME, "password", p)


# ── Credential dialog ─────────────────────────────────────────────────────────

def ask_credentials(prefill_user="", prefill_pass=""):
    root = tk.Tk()
    root.withdraw()

    dlg = tk.Toplevel(root)
    dlg.title("IITBHU Login")
    dlg.resizable(False, False)
    dlg.grab_set()

    pad = {"padx": 10, "pady": 6}

    tk.Label(dlg, text="Username:").grid(row=0, column=0, sticky="e", **pad)
    user_var = tk.StringVar(value=prefill_user)
    user_entry = tk.Entry(dlg, textvariable=user_var, width=28)
    user_entry.grid(row=0, column=1, **pad)

    tk.Label(dlg, text="Password:").grid(row=1, column=0, sticky="e", **pad)
    pass_var = tk.StringVar(value=prefill_pass)
    tk.Entry(dlg, textvariable=pass_var, show="•", width=28).grid(row=1, column=1, **pad)

    result = {}

    def on_ok():
        result["u"] = user_var.get().strip()
        result["p"] = pass_var.get()
        dlg.destroy()
        root.destroy()

    def on_cancel():
        root.destroy()

    btn = tk.Frame(dlg)
    btn.grid(row=2, column=0, columnspan=2, pady=8)
    tk.Button(btn, text="  OK  ", command=on_ok, width=8).pack(side="left", padx=6)
    tk.Button(btn, text="Cancel", command=on_cancel, width=8).pack(side="left", padx=6)

    dlg.protocol("WM_DELETE_WINDOW", on_cancel)
    user_entry.focus_set()
    root.mainloop()

    return result.get("u"), result.get("p")


# ── Network ───────────────────────────────────────────────────────────────────

def do_post_login(url, username, password):
    s = requests.Session()
    r = s.post(url, data={FIELD_USER: username, FIELD_PASS: password},
                timeout=15, allow_redirects=True)
    r.raise_for_status()
    return s


def ping_keepalive(url):
    try:
        requests.get(url, timeout=10)
    except Exception:
        pass  # silent — will retry next interval


# ── FreeFileSync ──────────────────────────────────────────────────────────────

def launch_ffs():
    if not os.path.isfile(FFS_EXE):
        messagebox.showerror("FreeFileSync not found", f"Expected:\n{FFS_EXE}")
        return
    if not os.path.isfile(FFS_CONFIG):
        messagebox.showerror("Config not found", f"Expected:\n{FFS_CONFIG}")
        return
    subprocess.Popen([FFS_EXE, FFS_CONFIG])


# ── System tray ───────────────────────────────────────────────────────────────

def make_tray_icon():
    img = Image.new("RGB", (64, 64), color=(30, 100, 200))
    d = ImageDraw.Draw(img)
    d.ellipse([8, 8, 56, 56], fill=(255, 255, 255))
    d.text((22, 18), "IIT", fill=(30, 100, 200))
    return img


def run_tray(stop_event):
    def quit_action(icon, item):
        stop_event.set()
        icon.stop()

    icon = pystray.Icon(
        "IITBHU_Sync",
        make_tray_icon(),
        "IITBHU Connected",
        menu=pystray.Menu(pystray.MenuItem("Quit", quit_action)),
    )
    icon.run()
    stop_event.set()


# ── Keepalive loop ────────────────────────────────────────────────────────────

def keepalive_loop(stop_event):
    while not stop_event.is_set():
        url = read_url()
        if "keepalive" in url:
            ping_keepalive(url)
        stop_event.wait(KEEPALIVE_INTERVAL)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    url = read_url()
    saved_user, saved_pass = load_credentials()

    # Always show dialog pre-filled with saved credentials
    username, password = ask_credentials(saved_user, saved_pass)
    if not username:
        sys.exit(0)
    save_credentials(username, password)

    # If current URL is a login URL, POST credentials
    if "login" in url:
        try:
            do_post_login(url, username, password)
        except requests.HTTPError as e:
            messagebox.showerror("Login failed", f"Server returned {e.response.status_code}.\nCheck your credentials.")
            return
        except requests.ConnectionError:
            messagebox.showerror("Connection error", f"Cannot reach:\n{url}\n\nAre you on the IITBHU network?")
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # Wait briefly for url_home.txt to update to keepalive URL
        time.sleep(3)

    # Launch FreeFileSync
    launch_ffs()

    # Start keepalive loop + system tray
    stop_event = threading.Event()
    threading.Thread(target=keepalive_loop, args=(stop_event,), daemon=True).start()
    run_tray(stop_event)   # blocks until user clicks Quit


if __name__ == "__main__":
    main()
