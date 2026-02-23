from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(model_name = "openai/gpt-oss-120b", api_key = API_KEY)

def agen_sisd(query):
    print(f"Memprroses (SISD)...")
    now = time.time()
    
    response = llm.invoke(query)
    last = time.time() - now
    
    return response.content, last

hasil, last = agen_sisd("Jelaskan apa itu Single intruksi, single data")

print("---- JAWABAN DARI LLM DENGAN SINGLE CORE, SINGLE INTRUCTION ----")
print(hasil)
print(f"---- WAKTU : {last}----")