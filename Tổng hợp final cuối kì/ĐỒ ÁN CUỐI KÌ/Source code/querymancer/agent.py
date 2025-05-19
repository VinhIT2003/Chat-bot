from datetime import datetime
from typing import List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from querymancer.custom_logging import green_border_style, log_panel
from querymancer.tools import call_tool

SYSTEM_PROMPT = f"""
You are Querymancer, a master database engineer with exceptional expertise in Microsoft SQL Server query construction and optimization.
Your purpose is to transform natural language requests into precise, efficient SQL queries that deliver exactly what the user needs.

<instructions>
<instruction>Use SQL Server syntax. Do NOT use LIMIT. Use SELECT TOP n instead.</instruction>
<instruction>Devise your own strategic plan to explore and understand the database before constructing queries.</instruction>
<instruction>Determine the most efficient sequence of database investigation steps based on the specific user request.</instruction>
<instruction>Independently identify which database elements require examination to fulfill the query requirements.</instruction>
<instruction>Formulate and validate your query approach based on your professional judgment of the database structure.</instruction>
<instruction>Only execute the final SQL query when you’ve thoroughly validated its correctness and efficiency.</instruction>
<instruction>Balance comprehensive exploration with efficient tool usage to minimize unnecessary operations.</instruction>
<instruction>For every tool call, include a detailed reasoning parameter explaining your strategic thinking.</instruction>
<instruction>Be sure to specify every required parameter for each tool call.</instruction>
<instruction>All table and column names in SQL queries must be written in lowercase.</instruction>
</instructions>

Today is {datetime.now().strftime("%Y-%m-%d")}

Your responses should be formatted as Markdown. Prefer using tables or lists for displaying data where appropriate.
Your target audience is business analysts and data scientists who may not be familiar with SQL syntax.
""".strip()

def create_history() -> List[BaseMessage]:
    return [SystemMessage(content=SYSTEM_PROMPT)]

def ask(query: str, history: List[BaseMessage], llm: BaseChatModel, max_iterations: int = 10) -> str:
    log_panel(
        title="User Request",
        content=f"Query: {query}",
        border_style=green_border_style
    )

    _iterations = 0
    messages = history.copy()
    messages.append(HumanMessage(content=query))

    while _iterations < max_iterations:
        response = llm.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            return response.content

        for tool_call in response.tool_calls:
            response = call_tool(tool_call)
            messages.append(response)
        
        _iterations += 1

    raise RuntimeError("Maximum number of iterations reached. Please try again with a different query.")

# tại sao nó gọi hàm tool
# tại sao nó trả lời được


# from datetime import datetime
# from typing import List

# from langchain_core.language_models.chat_models import BaseChatModel
# from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

# from querymancer.custom_logging import green_border_style, log_panel
# from querymancer.tools import call_tool

# # Thêm: thư viện dịch tiếng Việt sang tiếng Anh
# from transformers import MarianMTModel, MarianTokenizer

# def translate_vi_to_en(text: str) -> str:
#     model_name = 'Helsinki-NLP/opus-mt-vi-en'
#     tokenizer = MarianTokenizer.from_pretrained(model_name)
#     model = MarianMTModel.from_pretrained(model_name)

#     tokens = tokenizer(text, return_tensors="pt", padding=True)
#     translated = model.generate(**tokens)

#     return tokenizer.decode(translated[0], skip_special_tokens=True)

# from transformers import MarianTokenizer, MarianMTModel

# def translate_en_to_vi(text: str, llm: BaseChatModel) -> str:
#     prompt = f"""
# Bạn là một dịch giả chuyên nghiệp. Hãy dịch chính xác từng dòng sau từ tiếng Anh sang tiếng Việt.

# Yêu cầu:
# - Không thêm bất kỳ thông tin nào.
# - Không suy diễn hay giải thích thêm.
# - Giữ nguyên cấu trúc gốc của văn bản, đặc biệt là với các truy vấn SQL.

# Văn bản cần dịch:
# {text}
# """
#     return llm.invoke(prompt).content



# SYSTEM_PROMPT = f""" 
# You are Querymancer, a master database engineer with exceptional expertise in Microsoft SQL Server query construction and optimization. 
# Your purpose is to transform natural language requests into precise, efficient SQL queries that deliver exactly what the user needs.

# <instructions>
# <instruction>Use SQL Server syntax. Do NOT use LIMIT. Use SELECT TOP n instead.</instruction>
# <instruction>Devise your own strategic plan to explore and understand the database before constructing queries.</instruction>
# <instruction>Determine the most efficient sequence of database investigation steps based on the specific user request.</instruction>
# <instruction>Independently identify which database elements require examination to fulfill the query requirements.</instruction>
# <instruction>Formulate and validate your query approach based on your professional judgment of the database structure.</instruction>
# <instruction>Only execute the final SQL query when you’ve thoroughly validated its correctness and efficiency.</instruction>
# <instruction>Balance comprehensive exploration with efficient tool usage to minimize unnecessary operations.</instruction>
# <instruction>For every tool call, include a detailed reasoning parameter explaining your strategic thinking.</instruction>
# <instruction>Be sure to specify every required parameter for each tool call.</instruction>
# <instruction>All table and column names in SQL queries must be written in lowercase.</instruction>
# </instructions>

# Today is {datetime.now().strftime("%Y-%m-%d")}

# Your responses should be formatted as Markdown. Prefer using tables or lists for displaying data where appropriate.
# Your target audience is business analysts and data scientists who may not be familiar with SQL syntax.
# """.strip()

# def create_history() -> List[BaseMessage]:
#     return [SystemMessage(content=SYSTEM_PROMPT)]

# def ask(query: str, history: List[BaseMessage], llm: BaseChatModel, max_iterations: int = 100) -> str:
#     # Thêm bước dịch
#     translated_query = translate_vi_to_en(query)

#     log_panel(
#         title="User Request",
#         content=f"Original (VI): {query}\nTranslated (EN): {translated_query}",
#         border_style=green_border_style
#     )

#     _iterations = 0
#     messages = history.copy()
#     messages.append(HumanMessage(content=translated_query))

#     while _iterations < max_iterations:
#         response = llm.invoke(messages)
#         messages.append(response)

#         if not response.tool_calls:
#             return response.content

#         for tool_call in response.tool_calls:
#             response = call_tool(tool_call)
#             messages.append(response)
        
#         _iterations += 1

#     raise RuntimeError("Maximum number of iterations reached. Please try again with a different query.")



