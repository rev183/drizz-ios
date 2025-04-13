from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam, ChatCompletionAssistantMessageParam, \
    ChatCompletionSystemMessageParam

from constants import OPENAI_API_KEY
from steps import AppiumPlan, APPIUM_ACTIONS, AppiumStep

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


def generate_steps(steps: str):
    system_prompt = """Suppose you are a iOS tester following given instructions. Don't make up steps, interpret only given input"""
    assistant_prompt = f"""Format answer into steps which can be one of {APPIUM_ACTIONS} strictly"""
    prompt = f'Convert given instructions - {steps} without any unnecessary steps'

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            ChatCompletionUserMessageParam(role="user", content=prompt),
            ChatCompletionAssistantMessageParam(role="assistant", content=assistant_prompt),
            ChatCompletionSystemMessageParam(role="system", content=system_prompt)
        ],
        temperature=0.7,
        # max_tokens=2500,
        response_format=AppiumPlan,
    )
    out = response.choices[0].message.parsed
    print(out)
    return out


def find_element_in_xml(xml: str, step: AppiumStep):
    system_prompt = """Given XML is description of screen recorded using Appium iOS xcuitest driver"""
    assistant_prompt = f"""For the correctly found xml element. Give answer strictly as 'name' field of the element"""
    prompt = f"""Find the element in given xml: {xml} on which action {step.action} with input: {step.inputs} should be performed and answer with the single possible xml element"""

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            ChatCompletionUserMessageParam(role="user", content=prompt),
            ChatCompletionAssistantMessageParam(role="assistant", content=assistant_prompt),
            ChatCompletionSystemMessageParam(role="system", content=system_prompt),
        ],
        temperature=0.7,
        # max_tokens=2500,
    )
    out = response.choices[0].message.content
    return out
