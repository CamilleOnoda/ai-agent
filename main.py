import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("Welcome! It looks like something is missing!")
        print("\nUsage: python3 main.py 'Your Prompt'")
        print("\nExample: python3 main.py 'Why the sky is blue?'")
        sys.exit(1)
    user_prompt = sys.argv[1]
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    generate_content(user_prompt, messages, client)


def generate_content(user_prompt, messages, client):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
        )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    flag = "--verbose"

    print(f"Response :")
    print(response.text)
    if len(sys.argv) > 2 and sys.argv[2] == flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
