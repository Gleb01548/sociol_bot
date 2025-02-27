import re

import gradio as gr
from loguru import logger
from langchain import PromptTemplate

from src.service.context_search import ContextSearch


think_pattern = r"<think>(.*?)</think>"

context_search = ContextSearch(collection_name="social", qdrant_url="localhost")


system_template = """
**Роль**
Ты консультируешь людей о результатах социалогических исследований в России.
Ответ пиши только на РУССКОМ языке!

**Задача**
Твоя задача ответить на вопрос пользователя. Прежде чем давать ответ на
вопрос пользователя изучи переданный тебе контекст. Контекст состоит из
вопросов других граждан и ответов на них других граждан.

**Контекст**
{context}
"""


def predict(message, history):
    history = []
    print("message", message)
    print("history", history)
    context = context_search.create_context(user_message=message)
    #     system_prompt = (
    #         PromptTemplate(
    #             template=system_template,
    #             partial_variables={"user_message": message, "context": context},
    #         )
    #         .format_prompt()
    #         .text
    #     )

    #     answer = llm.generate(
    #         chat=[
    #             {
    #                 "role": "system",
    #                 "content": system_prompt,
    #             },
    #             {"role": "user", "content": message},
    #         ]
    #     )
    #     logger.info(f"Ответ модели: {answer}")
    #     final_response = re.sub(think_pattern, "", answer, flags=re.DOTALL).strip()
    #     final_response = f"""
    # Контекст
    # {context}

    # Ответ модели
    # {answer}
    # """
    return context[0]


demo = gr.ChatInterface(predict, type="messages")

demo.launch(share=False)
