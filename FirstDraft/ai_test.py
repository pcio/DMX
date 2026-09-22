from ollama import chat


response = chat(
    model="qwen3:1.7b",
    messages=[
        {
            "role": "user",
            "content": "Say hello in Danish."
        }
    ]
)

print(response.message.content)