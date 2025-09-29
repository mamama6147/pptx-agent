from pydantic import BaseModel, Field


# ストーリーの評価結果を表すデータモデル
class Judgement(BaseModel):
    judge: bool = Field(default=False, description="ストーリーが十分かどうかの判定結果")
    reason: str = Field(default="", description="ストーリーが十分かどうかの判定理由")


# ステートを表すデータモデル
class State(BaseModel):
    user_request: str = Field(..., description="ユーザーからのリクエスト")
    story: str = Field(default="", description="生成されたストーリー")
    iteration: int = Field(default=0, description="ストーリー生成の反復回数")
    current_judge: bool = Field(default=False, description="ストーリーが十分かどうかの判定結果")
    judgement_reason: str = Field(default="", description="ストーリーが十分かどうかの判定理由")
    slide_contents: str = Field(default="", description="スライドの内容")
    slide_gen_code: str = Field(default="", description="スライド生成のコード")
