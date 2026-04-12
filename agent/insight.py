import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_insight(question, df):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a business analyst. Given a question and data, write exactly one sentence of insight. Be specific with numbers. No fluff."
            },
            {
                "role": "user",
                "content": f"Question: {question}\nData:\n{df.to_string()}"
            }
        ]
    )
    return response.choices[0].message.content.strip()