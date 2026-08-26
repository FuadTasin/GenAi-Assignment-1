from langchain_core.prompts import PromptTemplate
from schemas import pydantic_output_parser

general_template=PromptTemplate(
    template="""
    You are an AI Tutor.
    The question given by the user is:
    {user_input}
    The user wants the explanation in the following category:
    {category_input}
    And also, the user wants the explanation at this level:
    {input_type}
    Give the response in a general way. Include mathematical equations or programming concepts when relevant.
    In this category, theoretical information should be prioritized over other types of information.
    """,
    input_variables=["user_input","input_type","category_input"],
)

mathematical_template=PromptTemplate(
    template="""
    You are an AI Tutor.
    The question given by the user is:
    {user_input}
    The user wants the explanation in the following category:
    {category_input}
    And also, the user wants the explanation at this level:
    {input_type}
    Give the response in a mathematical way. Theoretical concepts or programming knowledge may be included when relevant, but mathematical concepts and terminology should be prioritized.
    For better understanding, provide explanations alongside the equations.
    """,
    input_variables=["user_input","input_type","category_input"],
)

programming_template=PromptTemplate(
    template="""
    You are an AI Tutor.
    The question given by the user is:
    {user_input}
    The user wants the explanation in the following category:
    {category_input}
    And also, the user wants the explanation at this level:
    {input_type}
    Give a general idea about the program, including its approach, where it is used, and how it works. Then provide the program code with a short explanation.
    Prioritize the program code and its explanation, but also provide a brief general overview.
    """,
    input_variables=["user_input","input_type","category_input"],
)

summary_prompt=PromptTemplate(
    template="""
    You are an AI Tutor.
    Based on the user's question, give the proper summary of the question:
    {summary}
    Also follow the format instructions: 
    {format_instruction}
    """,
    input_variables=["user_input","summary"],
    partial_variables={"format_instruction":pydantic_output_parser.get_format_instructions,}
)

answer_prompt=PromptTemplate(
    template="""
    You are an AI Tutor.
    Based on the user's question, give the proper & elaborate answer of it:
    {answer}
    Also follow the format instructions: 
    {format_instruction}
    """,
    input_variables=["answer"],
    partial_variables={"format_instruction":pydantic_output_parser.get_format_instructions,}
)