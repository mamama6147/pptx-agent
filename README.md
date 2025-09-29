# パワーポイント自動生成AIエージェント

LangChainとLangGraphを使用して、ユーザーの入力からパワーポイント資料を自動生成するAIエージェントです。

## 参考記事

このプロジェクトは以下の記事を参考に作成しました:
- [パワポ資料自動作成AIエージェントを自作してみた](https://zenn.dev/aidemy/articles/69af8390f6ec3b)

## 機能

1. ユーザーの入力からプレゼンストーリーを作成
2. ストーリーの評価と改善(最大5回まで反復)
3. スライド内容の生成
4. python-pptxを使用したPythonコード生成

## 環境

- Python 3.10以上
- OpenAI API Key が必要

## インストール

```bash
pip install -r requirements.txt
```

## 環境変数の設定

```bash
export OPENAI_API_KEY="your-api-key"
```

## 使い方

1. プレゼンしたい内容をテキストファイルに記述(.txt, .md, .docx)
2. 以下のコマンドで実行:

```bash
python main.py --file input.txt
```

3. `output/create_pptx.py` が生成されるので実行:

```bash
python output/create_pptx.py
```

4. パワーポイントファイルが生成されます!

## ファイル構成

- `datamodel.py`: データモデルの定義
- `story_generator.py`: ストーリー作成ノード
- `story_evaluator.py`: ストーリー評価ノード
- `slide_contents_generator.py`: スライド内容作成ノード
- `pptx_code_generator.py`: Pythonコード作成ノード
- `pptx_agent.py`: ワークフロー(グラフ)の定義
- `main.py`: 実行ファイル

## ワークフロー

```
ユーザー入力 → ストーリー作成 → ストーリー評価 → スライド内容作成 → Pythonコード生成
                      ↑________________|
                    (評価NGの場合、最大5回まで)
```

## 改善案

- パワーポイントテンプレートの使用
- 画像のプリセット or AI生成
- アイコンのプリセット化
- 生成コードのエラーハンドリング

## ライセンス

MIT
