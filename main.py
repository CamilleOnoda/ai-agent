import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

FLAG = "--verbose"


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
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    for i in range(21):
        try:
            response = generate_content(user_prompt, messages, client, system_prompt, available_functions)
            if not response.function_calls:
                print("Final response:")
                print(response.text)
                break

            # If no final text response: the model wants to call tools
            for candidate in response.candidates:
                # Add model's turn which contains the function call
                messages.append(candidate.content)

                # Iterate through the parts of candidate's content
                # to find a function_call and execute
                for part in candidate.content.parts:
                    if part.function_call:
                        function_call_object = part.function_call
                        if len(sys.argv) > 2 and sys.argv[2] == FLAG:
                            tool_response_message = call_function(function_call_object, FLAG)
                        else:
                            tool_response_message = call_function(function_call_object)

                        messages.append(tool_response_message)

        except Exception as e:
            print(f"error: {e}")
  

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    args = function_call.args.copy()
    args["working_directory"] = "./calculator"
    function_dic = {
        "get_files_info":get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    result = function_dic[function_call.name](**args)

    if not function_call.name in function_dic:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                    )
                ],
            )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": result},
                    )
                ],
            )


def generate_content(user_prompt, messages, client, system_prompt, available_functions):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            )
        )
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    
    if len(sys.argv) > 2 and sys.argv[2] == FLAG:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    return response


if __name__ == "__main__":
    main()
