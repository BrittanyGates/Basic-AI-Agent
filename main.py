from call_function import call_function, available_functions
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


def main():
    if len(sys.argv) < 2:
        print("Error: Missing prompt")
        sys.exit(1)

    is_verbose = "--verbose" in sys.argv
    user_prompt = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    system_prompt = """
    You are a helpful AI coding agent. Your primary goal is to answer questions and fulfill requests about the codebase. To do this, you must first explore the codebase to understand its structure and content.

    **Always start by using the available tools to explore the files and directories.**

    You can perform the following operations:
    - `get_files_info`: to list files and directories.
    - `get_file_content`: to read the contents of a file.
    - `run_python_file`: to execute a python file.
    - `write_file`: to write to a file.

    When a user asks a question, follow these steps:
    1.  Use `get_files_info` to list the files in the current directory or a subdirectory.
    2.  Identify relevant files based on their names.
    3.  Use `get_file_content` to read the contents of the relevant files.
    4.  Analyze the code to answer the user's question.
    5.  If necessary, use `run_python_file` to execute code and verify your understanding.
    6.  Formulate your answer based on the information you have gathered.

    Do not ask the user for information you can obtain yourself by using the available tools. All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    print(f"User: {user_prompt}")

    turn_count = 0
    while True:
        turn_count += 1
        if turn_count > 20:
            print("Loop terminated: Maximum 20 iterations reached.")
            break
        try:
            response = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages,
                                                      config=types.GenerateContentConfig(tools=[available_functions],
                                                                                         system_instruction=system_prompt))
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count

            if is_verbose:
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")

            if response.function_calls:
                print(f"Model: I want to call {response.function_calls[0].name}...")
                tool_responses = []
                for item in response.function_calls:
                    function_call_result = call_function(item, verbose=is_verbose)

                    if (
                            not function_call_result.parts
                            or not function_call_result.parts[0].function_response
                    ):
                        raise Exception("Function call did not return a response")

                    if is_verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")

                    tool_responses.append(function_call_result.parts[0])

                if not tool_responses:
                    raise Exception("No function responses generated, exiting.")

                for candidate in response.candidates:
                    messages.append(candidate.content)
                messages.append(types.Content(role="user", parts=tool_responses))
            else:
                print(f"Model: {response.text}")
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    main()
