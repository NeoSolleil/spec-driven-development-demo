"""
frontend_greeting.feature に対応するE2Eテスト（Playwright）。
BE APIを起動 → 画面を開く → ボタン操作 → 表示を検証。
"""
import os, sys, time, subprocess, http.server, socketserver, threading
from playwright.sync_api import sync_playwright

BACKEND = os.path.join(os.path.dirname(__file__), "..", "..", "backend")
FRONTEND = os.path.join(os.path.dirname(__file__), "..")


def _start_backend():
    """BE APIサーバーを起動"""
    proc = subprocess.Popen(
        [sys.executable, "app.py"], cwd=os.path.abspath(BACKEND),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(2)  # 起動待ち
    return proc


def _start_frontend():
    """FE（静的HTML）を簡易サーバーで配信"""
    os.chdir(os.path.abspath(FRONTEND))
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", 8000), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def test_画面操作であいさつと履歴が出る():
    backend = _start_backend()
    frontend = _start_frontend()
    try:
        with sync_playwright() as p:
            page = p.chromium.launch().new_page()
            page.goto("http://localhost:8000/index.html")  # Given 画面を開く

            page.click("button[data-number='2']")           # When 日本語
            page.wait_for_function(
                "document.querySelector('#greeting').textContent === 'こんにちは、世界！'"
            )
            assert page.inner_text("#greeting") == "こんにちは、世界！"  # Then 表示

            page.click("button[data-number='1']")           # And 英語
            page.wait_for_function(
                "document.querySelectorAll('#history li').length === 2"
            )
            items = page.locator("#history li").all_inner_texts()
            assert items == ["こんにちは、世界！", "Hello, World!"]   # Then 履歴順
    finally:
        backend.terminate()
        frontend.shutdown()
