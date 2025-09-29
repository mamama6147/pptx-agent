import argparse
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pptx_agent import PPTXAgent

# .envファイルから環境変数を読み込む
load_dotenv()


def main():
    # コマンドライン引数のパーサーを作成
    parser = argparse.ArgumentParser(
        description="ユーザーがインプットしたテキストを基にスライドを生成するPythonファイルを出力します"
    )

    # "file"引数を追加
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="プレゼンテーションの元になるテキストファイルのパス(.txt/.docx/.md)"
    )

    # コマンドライン引数を解析
    args = parser.parse_args()

    # OpenAI API Keyの確認
    if not os.getenv("OPENAI_API_KEY"):
        print("エラー: OPENAI_API_KEY環境変数が設定されていません")
        print("\n設定方法:")
        print("1. プロジェクトルートに .env ファイルを作成")
        print("2. 以下の内容を記述:")
        print('   OPENAI_API_KEY=your-api-key-here')
        print("\nまたは、コマンドラインで設定:")
        print('   export OPENAI_API_KEY="your-api-key"')
        return

    # テキストの取得
    filepath = args.file
    if filepath.endswith((".txt", ".md")):
        with open(filepath, "r", encoding="utf-8") as f:
            user_request = f.read()
    elif filepath.endswith(".docx"):
        # docxファイルの読み込みには python-docx が必要
        try:
            from docx import Document
            doc = Document(filepath)
            user_request = "\n".join([para.text for para in doc.paragraphs])
        except ImportError:
            print("エラー: .docxファイルを読み込むには python-docx をインストールしてください")
            print("pip install python-docx")
            return
    else:
        raise ValueError("ファイル形式がサポートされていません(.txt, .md, .docxのみ対応)")

    print(f"入力ファイル: {filepath}")
    print(f"入力テキスト長: {len(user_request)}文字\n")

    # ChatOpenAIモデルを初期化
    print("AIエージェントを初期化中...")
    llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

    # PPTXAgentを初期化
    agent = PPTXAgent(llm=llm)

    # エージェントを実行して最終的な出力を取得
    print("\nエージェントを実行中...")
    print("1. ストーリー作成")
    print("2. ストーリー評価")
    print("3. スライド内容生成")
    print("4. Pythonコード生成\n")

    final_output = agent.run(user_request=user_request)

    # コードブロックから実際のPythonコードを抽出
    if "```python" in final_output:
        final_output = final_output.split("```python\n")[-1].split("```")[0]
    elif "```" in final_output:
        final_output = final_output.split("```")[-2]

    # 出力ディレクトリの作成
    os.makedirs("output", exist_ok=True)

    # 出力をファイルに保存
    output_path = "output/create_pptx.py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_output)

    print(f"\n完了! 生成されたPythonコードを {output_path} に保存しました")
    print("\n次のステップ:")
    print(f"  python {output_path}")
    print("\nを実行すると output.pptx が生成されます!")


if __name__ == "__main__":
    main()
