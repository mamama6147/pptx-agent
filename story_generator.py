from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


class StoryGenerator:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def run(self, user_request: str) -> str:
        # プロンプトを定義
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはプレゼンテーションのストーリーを作成する専門家です。"
                ),
                (
                    "human",
                    "以下のユーザーリクエストに基づいて、プレゼンテーションのストーリーを作成してください。\n\n"
                    "ユーザーの意図を理解し、その意図がオーディエンスにしっかりと伝わることを重視してください。\n\n"
                    "ユーザーリクエスト:\n{user_request}"
                )
            ]
        )

        # ストーリー作成のためのチェーンを作成
        chain = prompt | self.llm | StrOutputParser()

        # ストーリーを生成
        return chain.invoke({"user_request": user_request})
