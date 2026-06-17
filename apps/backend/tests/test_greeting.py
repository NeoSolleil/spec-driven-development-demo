"""backend_greeting.feature に対応するロジックのテスト（pytest）"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from greeting import GreetingService

def test_日本語を取得する():
    s = GreetingService()
    assert s.greet(2) == "こんにちは、世界！"

def test_対応外はデフォルト英語():
    s = GreetingService()
    assert s.greet(99) == "Hello, World!"

def test_履歴が取得順に並ぶ():
    s = GreetingService()
    s.greet(2)
    s.greet(1)
    assert s.history() == ["こんにちは、世界！", "Hello, World!"]
