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

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/mamama6147/pptx-agent.git
cd pptx-agent
```

### 2. 必要なライブラリをインストール

```bash
pip install -r requirements.txt
```

### 3. APIキーの設定

プロジェクトルートに `.env` ファイルを作成し、OpenAI API Keyを設定します:

```bash
# .envファイルを作成
cp .env.example .env
```

`.env` ファイルを編集して、実際のAPIキーを設定:

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxx
```

**注意**: `.env` ファイルは `.gitignore` に含まれているため、Gitにコミットされません。

#### APIキーの取得方法

1. [OpenAI Platform](https://platform.openai.com/) にアクセス
2. アカウントを作成/ログイン
3. API Keys セクションで新しいキーを生成

## 使い方

### 基本的な使い方

1. プレゼンしたい内容をテキストファイルに記述(.txt, .md, .docx)

```txt
AIエージェントの基礎について、初心者向けのプレゼンテーションを作成してください。

以下の内容を含めてください:
- AIエージェントとは何か
- AIエージェントの基本的な構成要素
- 実際の活用事例
- 今後の展望
```

2. エージェントを実行:

```bash
python main.py --file example_input.txt
```

3. 生成された `output/create_pptx.py` を実行:

```bash
python output/create_pptx.py
```

4. `output.pptx` が生成されます!

## ファイル構成

```
pptx-agent/
├── README.md                      # このファイル
├── requirements.txt               # 必要なライブラリ
├── .env.example                   # 環境変数のテンプレート
├── .gitignore                     # Git管理除外設定
├── example_input.txt              # サンプル入力ファイル
├── main.py                        # 実行ファイル
├── pptx_agent.py                  # ワークフロー(グラフ)の定義
├── datamodel.py                   # データモデルの定義
├── story_generator.py             # ストーリー作成ノード
├── story_evaluator.py             # ストーリー評価ノード
├── slide_contents_generator.py    # スライド内容作成ノード
└── pptx_code_generator.py         # Pythonコード作成ノード
```

## ワークフロー

```
ユーザー入力 → ストーリー作成 → ストーリー評価 → スライド内容作成 → Pythonコード生成
                      ↑________________|
                    (評価NGの場合、最大5回まで)
```

## トラブルシューティング

### API Keyエラーが出る場合

```
エラー: OPENAI_API_KEY環境変数が設定されていません
```

→ `.env` ファイルが正しく作成されているか確認してください

### モジュールが見つからないエラー

```
ModuleNotFoundError: No module named 'xxx'
```

→ `pip install -r requirements.txt` を再度実行してください

## 改善案

記事で提案されている改善案:

- パワーポイントテンプレートの使用
- 画像のプリセット or AI生成
- アイコンのプリセット化
- 生成コードのエラーハンドリング

## ライセンス

MIT
