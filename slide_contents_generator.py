from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class SlideContentsGenerator:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def run(self, user_request: str, story: str) -> str:
        # プロンプトを定義
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは提供されたストーリーに基づいてプレゼンテーションの構成を作成する専門家です。"
                ),
                (
                    "human",
                    "以下のユーザーリクエストと生成されたストーリーに基づいて、プレゼンテーションのスライドの内容を作成してください。\n\n"
                    "ユーザーリクエスト: {user_request}\n\n"
                    "ストーリー:\n{story}\n\n"
                    "ルール:\n"
                    "- スライドの内容は、テキストベースで作成してください。\n"
                    "- 使用して良いのはテキスト、図形、表のみです。\n"
                    "- テキスト以外の要素(図形および表)を使用する場合は、その旨を明記してください。\n"
                    "- スライド番号を進める際は、'---next---' と記述してください。\n\n"
                )
            ]
        )

        # スライド内容を生成するチェーンを作成
        chain = prompt | self.llm | StrOutputParser()

        # スライド内容を生成
        return chain.invoke({"user_request": user_request, "story": story})
