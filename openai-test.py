from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a primary care pharmacist at Alto Pharmacy."},
    {"role": "user", "content": "What is the best OTC medication for a common migraine?"}
  ]
)

print(completion.choices[0].message)