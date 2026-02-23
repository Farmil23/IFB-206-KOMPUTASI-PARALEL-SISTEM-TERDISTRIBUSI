
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import time
from concurrent.futures import ThreadPoolExecutor
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatGroq(model_name = "openai/gpt-oss-120b", api_key = API_KEY)

def task_1():
    print("---TASK 1---")
    return llm.invoke("Jelaskan siapa Farhan kamil hermansyah").content

def task_2():
    print("---TASK 2---")
    return llm.invoke("Apa bedanya SISD dengan SIMD?").content

def task_3():
    print("---TASK 3---")
    return llm.invoke("berikan ide menarik tentang startup").content

if __name__ == "__main__":
    now = time.time()
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(task_1),
            executor.submit(task_2),
            executor.submit(task_3),
        ]
        for future in futures:
            print(future.result())
        
        times = time.time() - now
        print(f"---WAKTU : {times}")