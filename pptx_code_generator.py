from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class PPTXCodeGenerator:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def run(self, slide_contents: str) -> str:
        # プロンプトを定義
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "python-pptxモジュールを用いてプレゼンテーション資料のスライドを自動生成する専門家です。"
                ),
                (
                    "human",
                    "以下のスライドの内容を生成するためのpythonコードを生成してください。\n\n"
                    "スライドの内容:\n{slide_contents}\n\n"
                    "新しいプレゼンテーションを作成し、スライドを追加してください。\n"
                    "作成したパワーポイントは output.pptx として保存してください。\n\n"
                    "ルール:\n"
                    "- 【重要】必ずpython-pptxモジュールを使用したpythonコードのみを出力してください。\n"
                    "- 使用が許可されているのは、テキスト、図形、表のみです。\n"
                    "- テキスト以外の要素(図形および表)を使用してほしい箇所には、その旨が明記されています。\n"
                    "- 画像や動画は使用できません。絶対に画像や動画を使用しないでください。\n"
                    "- '---next---' はスライド番号を進める合図です。このタイミングで新たなスライドを追加してください。\n\n"
                )
            ]
        )

        # スライド生成のためのチェーンを作成
        chain = prompt | self.llm | StrOutputParser()

        # スライド生成のコードを生成
        return chain.invoke({"slide_contents": slide_contents})
