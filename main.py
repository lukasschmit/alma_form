import asyncio
import json
from enum import Enum

from browser_use import ActionResult, Agent, Browser, BrowserConfig
from browser_use.controller.service import Controller
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from data import MOCK_DATA
from decompose import get_form_instructions
from overfit import generate_overfitted_form_instructions


class DoneResult(BaseModel):
    success: bool
    description: str


class ModelType(Enum):
    CLAUDE = "claude"
    CHATGPT = "chatgpt"


class PromptType(Enum):
    OVERFIT = "overfit"  # overfit prompt engineering
    JSON = "json"  # agent gets raw json
    SINGLE_STEP = "single_step"  # english parsed from json
    DECOMPOSED = "decomposed"  # english parsed, each field is a separate step
    HYBRID = "hybrid"  # New hybrid mode


async def fill_form(
    base_url: str,
    form_data: dict,
    timeout: float,
    model_type: ModelType = ModelType.CHATGPT,
    temperature: float = 0.0,
    headless: bool = False,
    use_vision: bool = True,
    prompt_type: PromptType = PromptType.JSON,
    disable_security: bool = True,
    extra_rules: str = "",
) -> None:
    try:
        # Initialize the controller
        browser = Browser(
            config=BrowserConfig(headless=headless, disable_security=disable_security)
        )
        controller = Controller()

        # Add the done action
        @controller.registry.action("Done with task", param_model=DoneResult)
        async def done(params: DoneResult):
            result = ActionResult(
                is_done=True, extracted_content=params.model_dump_json()
            )
            print(result)
            return result

        # Select the model
        if model_type == ModelType.CHATGPT:
            model = ChatOpenAI(model="gpt-4o", temperature=temperature, seed=42)
        elif model_type == ModelType.CLAUDE:
            model = ChatAnthropic(
                model="claude-3-7-sonnet-latest", temperature=temperature
            )
        else:
            raise ValueError(f"Invalid model type: {model_type}")

        async with await browser.new_context() as context:
            # Initial navigation
            nav_task = f"Navigate to: '{base_url}'."
            agent = Agent(
                task=nav_task,
                llm=model,
                max_actions_per_step=100,
                controller=controller,
                browser=browser,
                browser_context=context,
                use_vision=False,
            )
            try:
                await asyncio.wait_for(agent.run(max_steps=100), timeout=timeout)
            except TimeoutError:
                print(
                    f"Timeout after {timeout} seconds while trying to navigate to {base_url}"
                )
                return

            if prompt_type == PromptType.OVERFIT:
                task = generate_overfitted_form_instructions(form_data)

                agent = Agent(
                    task=task,
                    llm=model,
                    max_actions_per_step=100,
                    controller=controller,
                    browser=browser,
                    browser_context=context,
                    use_vision=use_vision,
                    generate_gif=f"agent_history_{model_type.value}_{prompt_type.value}.gif",
                )
                try:
                    await asyncio.wait_for(agent.run(max_steps=100), timeout=timeout)
                except TimeoutError:
                    print(
                        f"Timeout after {timeout} seconds while trying to fill form at {base_url}"
                    )
                    return

            elif prompt_type == PromptType.JSON:
                task = f"""Complete the form on the page using the following JSON data as the source of truth.

Strategy:
Keep track of the last field in the JSON data that was successfully filled out.
If you get lost, find the last field which was successfully filled out and resume from there.

Rules:
- EVERY field in the JSON data is required.
- NEVER fill out any fields that are not present in the JSON data.
- ALWAYS fill out fields in the SAME order they appear in the JSON data.
- Infer the input type from the content of the page and the field name/type. For example, booleans are often checkboxes.
- After filling out the form, verify that all fields are filled out correctly.

{"Extra rules:" if extra_rules else ""}{extra_rules}

JSON data:
{json.dumps(form_data, indent=1)}"""
                agent = Agent(
                    task=task,
                    llm=model,
                    max_actions_per_step=100,
                    controller=controller,
                    browser=browser,
                    browser_context=context,
                    use_vision=use_vision,
                    generate_gif=f"agent_history_{model_type.value}_{prompt_type.value}.gif",
                )
                try:
                    await asyncio.wait_for(agent.run(max_steps=100), timeout=timeout)
                except TimeoutError:
                    print(
                        f"Timeout after {timeout} seconds while trying to fill form at {base_url}"
                    )
                    return

            elif prompt_type == PromptType.SINGLE_STEP:
                steps = get_form_instructions(form_data)
                task = "\n".join([nav_task] + steps)
                agent = Agent(
                    task=f"Extra rules:\n{extra_rules}\n\n{task}",
                    llm=model,
                    max_actions_per_step=10,
                    controller=controller,
                    browser=browser,
                    browser_context=context,
                    use_vision=use_vision,
                    generate_gif=f"agent_history_{model_type.value}_{prompt_type.value}.gif",
                )
                try:
                    await asyncio.wait_for(agent.run(max_steps=100), timeout=timeout)
                except TimeoutError:
                    print(
                        f"Timeout after {timeout} seconds while trying to fill form at {base_url}"
                    )
                    return

            elif prompt_type == PromptType.DECOMPOSED:
                steps = get_form_instructions(form_data)
                for i, step in enumerate(steps):
                    print(f"{step=}")
                    agent = Agent(
                        task=f"Extra rules:\n{extra_rules}\n\n{step}",
                        llm=model,
                        max_actions_per_step=10,
                        controller=controller,
                        browser=browser,
                        browser_context=context,
                        use_vision=use_vision,
                        generate_gif=f"agent_history_{model_type.value}_{prompt_type.value}_{i}.gif",
                    )
                    try:
                        agent_history_list = await asyncio.wait_for(
                            agent.run(max_steps=5), timeout=timeout
                        )
                        for action_result in agent_history_list.action_results():
                            if action_result.is_done:
                                extracted_content = json.loads(
                                    action_result.extracted_content
                                )
                                if not extracted_content.get("success"):
                                    print(f"Step failed: {step}")
                                    print(
                                        f"Extracted content: {extracted_content.get('description')}"
                                    )
                                    return
                    except TimeoutError:
                        print(f"Timeout after {timeout} seconds on step: {step}")
                        return

            elif prompt_type == PromptType.HYBRID:
                steps = get_form_instructions(form_data)
                for i, step in enumerate(steps):
                    print(f"Processing step {i + 1}/{len(steps)}: {step}")
                    task = f"""Use the following JSON data as the source of truth to complete the form on the page.

- Your task is to fill out ONLY the field specified by current step.
- Use the full JSON data to understand the context and ensure accuracy.
- If the field from the current step is not found in the JSON or on the page, report it and mark the task as done with success=False.
- Infer the input type (e.g., text, checkbox) from the page content and field name/type.
- After filling the field, verify it was filled correctly.

Full JSON data:
{json.dumps(form_data, indent=1)}

{"Extra rules:" if extra_rules else ""}{extra_rules}

CURRENT STEP (fill this and ONLY this field):
    {step}"""

                    agent = Agent(
                        task=task,
                        llm=model,
                        max_actions_per_step=3,
                        controller=controller,
                        browser=browser,
                        browser_context=context,
                        use_vision=use_vision,
                        generate_gif=f"agent_history_{model_type.value}_{prompt_type.value}_{i}.gif",
                    )
                    try:
                        agent_history_list = await asyncio.wait_for(
                            agent.run(max_steps=3), timeout=timeout
                        )
                        for action_result in agent_history_list.action_results():
                            if action_result.is_done:
                                extracted_content = json.loads(
                                    action_result.extracted_content
                                )
                                if not extracted_content.get("success"):
                                    print(f"Step failed: {step}")
                                    print(
                                        f"Extracted content: {extracted_content.get('description')}"
                                    )
                                    return
                    except TimeoutError:
                        print(f"Timeout after {timeout} seconds on step: {step}")
                        return
    finally:
        browser.close()


if __name__ == "__main__":
    EXTRA_RULES = """
- "associated_with_student" is a checkbox labeled with "3. I am associated with" followed by a text input.
"""

    asyncio.run(
        fill_form(
            "https://mendrika-alma.github.io/form-submission/",
            MOCK_DATA,
            headless=False,
            timeout=3600,
            model_type=ModelType.CHATGPT,
            use_vision=True,
            prompt_type=PromptType.OVERFIT,
            extra_rules="",
            # extra_rules=EXTRA_RULES,
        )
    )
    print("Finished filling form")
