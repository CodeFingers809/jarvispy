import openai, os
from config import apikey

openai.api_key = apikey

response = openai.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="write an essay on christmas",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
)

print(response.choices[0].text)
