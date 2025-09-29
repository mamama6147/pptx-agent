from typing import Any
from IPython.display import Image
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from datamodel import Judgement, State
from story_generator import StoryGenerator
from story_evaluator import StoryEvaluator
from slide_contents_generator import SlideContentsGenerator
from pptx_code_generator import PPTXCodeGenerator


class PPTXAgent:
    def __init__(self, llm: ChatOpenAI):
        # 各種ジェネレーターの初期化
        self.story_generator = StoryGenerator(llm=llm)
        self.story_evaluator = StoryEvaluator(llm=llm)
        self.slide_contents_generator = SlideContentsGenerator(llm=llm)
        self.pptx_code_generator = PPTXCodeGenerator(llm=llm)

        # グラフの作成
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        # グラフの初期化
        workflow = StateGraph(State)

        # 各ノードの追加
        workflow.add_node("generate_story", self._generate_story)
        workflow.add_node("evaluate_story", self._evaluate_story)
        workflow.add_node("generate_slide_contents", self._generate_slide_contents)
        workflow.add_node("generate_pptx_code", self._generate_pptx_code)

        # エントリーポイントの設定
        workflow.set_entry_point("generate_story")

        # ノード間のエッジの追加
        workflow.add_edge("generate_story", "evaluate_story")
        workflow.add_conditional_edges(
            "evaluate_story",
            lambda state: not state.current_judge and state.iteration < 5,
            {True: "generate_story", False: "generate_slide_contents"}
        )
        workflow.add_edge("generate_slide_contents", "generate_pptx_code")
        workflow.add_edge("generate_pptx_code", END)

        # グラフのコンパイル
        return workflow.compile()

    def _generate_story(self, state: State) -> dict[str, Any]:
        # ストーリーの生成
        new_story: str = self.story_generator.run(state.user_request)
        return {
            "story": new_story,
            "iteration": state.iteration + 1
        }

    def _evaluate_story(self, state: State) -> dict[str, Any]:
        # ストーリーの評価
        judgement: Judgement = self.story_evaluator.run(state.user_request, state.story)
        return {
            "current_judge": judgement.judge,
            "judgement_reason": judgement.reason
        }

    def _generate_slide_contents(self, state: State) -> dict[str, Any]:
        # スライド内容の生成
        slide_contents: str = self.slide_contents_generator.run(state.user_request, state.story)
        return {"slide_contents": slide_contents}

    def _generate_pptx_code(self, state: State) -> dict[str, Any]:
        # Python-pptxコードの生成
        pptx_code: str = self.pptx_code_generator.run(state.slide_contents)
        return {"slide_gen_code": pptx_code}

    def run(self, user_request: str) -> str:
        # 初期状態の設定
        initial_state = State(user_request=user_request)

        # グラフ構造の可視化(オプション)
        try:
            graph_img = Image(self.graph.get_graph().draw_png())
            with open("graph.png", "wb") as f:
                f.write(graph_img.data)
            print("ワークフローの可視化画像を graph.png として保存しました")
        except Exception as e:
            print(f"グラフの可視化に失敗しました: {e}")

        # グラフの実行
        final_state = self.graph.invoke(initial_state)

        # 最終的なPythonコードの取得
        return final_state["slide_gen_code"]
