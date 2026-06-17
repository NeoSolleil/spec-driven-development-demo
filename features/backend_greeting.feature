Feature: あいさつAPI

  Scenario: 日本語を取得する
    Given APIが起動している
    When POST /greet に番号 2 を送る
    Then "こんにちは、世界！" が返る

  Scenario: 対応外はデフォルト英語
    Given APIが起動している
    When POST /greet に番号 99 を送る
    Then "Hello, World!" が返る

  Scenario: 履歴が取得順に並ぶ
    Given APIが起動している
    When 番号 2、番号 1 の順であいさつを取得する
    Then GET /history は ["こんにちは、世界！", "Hello, World!"] を返す
