from groq import Groq
from json import load, dump
import datetime 
from dotenv import dotenv_values
import os
print("[DEBUG] Running from:", os.path.abspath(__file__))

env_vars = dotenv_values(".env")


Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GROQ_API_KEY")


# 4) initialize
client = Groq(api_key=GroqAPIKey)

#inkitialize an empty list yo store chat messages.
messages = []

#define a system message that provides context to the AI chatbot about its role and behaviour. 
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""


SystemChatBot = [
    {"role": "system", "content": System}
]


import json

try:
    with open(r"Data\ChatLog.json", "r") as f:
        content = f.read().strip()
        messages = json.loads(content) if content else []
except (FileNotFoundError, json.JSONDecodeError):
    messages = []
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f)


def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")


    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Time: {hour} hours :{minute} minutes :{second} second.\n"
    return data


def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI's response.""" 
    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)

        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7, 
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f, indent=4)

        return AnswerModifier(Answer=Answer)

    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        # Reset chat log to avoid corruption
        try:
            with open(r"Data\ChatLog.json", "w") as f:
                dump([], f, indent=4)
        except:
            pass
        # Instead of recursion, just return a clear message
        return "Sorry, Aurio encountered an internal error. Please try again."


if __name__=="__main__":
    while True:
        user_input = input("Enter Your Question:")
        print(ChatBot(user_input))