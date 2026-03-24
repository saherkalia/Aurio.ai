from googlesearch import search
from groq import Groq
from json import load, dump
import datetime 
from dotenv import dotenv_values


env_vars = dotenv_values(".env")


Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GROQ_API_KEY")


client = Groq(api_key=GroqAPIKey)


System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""


import json

try:
    with open(r"Data\ChatLog.json", "r") as f:
        content = f.read().strip()
        messages = json.loads(content) if content else []
except (FileNotFoundError, json.JSONDecodeError):
    messages = []
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f)


def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription:{i.description}\n\n"

    Answer += "[end]"
    return Answer


def AnsweModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [] 


def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data


def RealtimeSearchEngine(prompt):
    global messages

    # Load previous chat log
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)

    # Google search result as context
    search_context = GoogleSearch(prompt)

    # Construct prompt context
    system_messages = [
        {"role": "system", "content": System},
        {"role": "system", "content": search_context},
        {"role": "system", "content": Information()}
    ]

    # Add user query to chat history
    messages.append({"role": "user", "content": prompt})

    # Generate response
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=system_messages + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    # Save chat log
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    return AnsweModifier(Answer)    
    
if __name__=="__main__":
    while True:
        prompt = input("Enter your query:")
        print(RealtimeSearchEngine(prompt))

