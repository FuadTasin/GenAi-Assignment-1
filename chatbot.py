from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

chat_model=ChatGroq(model="openai/gpt-oss-120b",temperature=0.5)