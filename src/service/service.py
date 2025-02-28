import gradio as gr
from loguru import logger
from langchain import PromptTemplate

from src.service.context_search import ContextSearch
from src.models.model_api import use_min_max


context_search = ContextSearch(collection_name="social", qdrant_url="localhost")


system_template = """
**Роль**
Ты консультируешь людей о результатах социалогических исследований в России.
Ответ пиши только на РУССКОМ языке!

**Задача**
Твоя задача ответить на вопрос пользователя. Прежде чем давать ответ на
вопрос пользователя изучи переданный тебе контекст.

**Контекст**
{context}
"""


def predict(message, history):
    logger.info(f"Вопрос пользователя: {message}")
    context = context_search.create_context(user_message=message)[0]
    system_prompt = (
        PromptTemplate(
            template=system_template,
            partial_variables={"context": context},
        )
        .format_prompt()
        .text
    )

    answer = use_min_max(system_prompt=system_prompt, message=message)

    logger.info(f"Ответ модели: {answer}")

    final_response = f"""
## Найденный обзор

{context}


## Ответ модели

{answer}
    """
    logger.info(f"Финальный ответ: {final_response}")
    return final_response


demo = gr.ChatInterface(
    predict,
    type="messages",
    examples=[
        "Что россияне думали полиции в 2024 году?",
        "Материальный достаток россиян в 2024 году",
    ],
    title="Бот отвечает на основе данных ВЦИОМ (https://wciom.ru/analytical-reviews)"
)

demo.launch(share=True)
