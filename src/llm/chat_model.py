import os
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo-instruct", max_tokens=512)

prompt = input("Enter a prompt: ")

for chunk in llm.stream(prompt):
    print(chunk, end="", flush=True)