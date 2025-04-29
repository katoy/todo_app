# Todoアプリ

## 概要

このアプリは、シンプルなTodoリストです。

## 使い方

1. アプリを起動します。
2. Todoを追加します。
3. Todoを完了します。
4. Todoを削除します。

## スクリーンショット

![スクリーンショット](screenshots/001.png)

## ライセンス

このアプリは、MITライセンスで公開されています。

## 起動方法

```bash
python3 app.py
```

## テストの実行とカバレッジ計測方法

```bash
pthon3 -m coverage run -m pytest
pthon3 -m coverage report -m
```

## ファイル構成

```
.
├── .gitignore
├── LICENSE
├── README.md
├── app.py
├── static
│   ├── script.js
│   └── style.css
├── templates
│   └── index.html
├── tests
│   └── test_app.py
└── translations
    ├── en.json
    ├── ja.json
    └── zh.json
```

## その他

アプリケーション、テストコード、README、LICENSEファイルなどは、clineを利用して作成されました。
スクリーンショットは手動で作成しました。

##
github colilot や cline の使い方は次を参考にしました。

- https://www.youtube.com/watch?v=A6Dx8xXUcaA&t=1659s
  AIエージェント・MCPサーバも解説！VSCodeでAIを使ってみよう！プログラミングをAIで効率化 〜初心者向け〜
