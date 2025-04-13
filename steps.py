from pydantic import BaseModel


class InputStep(BaseModel):
    action: str
    origin_input: str

class InputPlan(BaseModel):
    steps: list[InputStep]

class AppiumStep(BaseModel):
    action: str
    inputs: list[str]

class AppiumPlan(BaseModel):
    steps: list[AppiumStep]

APPIUM_ACTIONS = ['navigate', 'tap', 'screenshot']