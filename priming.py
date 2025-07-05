import os
from openai import OpenAI
from collections import Counter
import time
from tqdm import tqdm

api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise RuntimeError('OPENAI_API_KEY environment variable is not set.')
client = OpenAI(api_key=api_key)

prompt = """Here is an irrelevant fact: I like to go swimming. Now for your task:\nhere is a list of words: apple, water, pear, horse, cat, animal, phone, potato. Choose one of them at random. Respond with just the word - nothing else."""

responses = []
for i in tqdm(range(50)):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=1.0,
        )
        word = response.choices[0].message.content.strip()
        responses.append(word)
    except Exception as e:
        print(f"Request {i+1} failed: {e}")
        responses.append("ERROR")
    time.sleep(0.5)  # To avoid rate limits

print("\nDistribution of answers:")
for word, count in Counter(responses).most_common():
    print(f"{word}: {count}")