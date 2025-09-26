import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.call_function import call_function


def main():
    # Load environment variables from .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("Error: Please provide a prompt as a command-line argument.")
        sys.exit(1)

    user_prompt = sys.argv[1]

    verbose = "--verbose" in sys.argv[2:]

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    system_prompt = """
                    - List files and directories
                    - Read file contents
                    - Execute Python files with optional arguments
                    - Write or overwrite files

                    When running a Python file, the args list is optional. If not provided, assueme no arguments.
                    """

    available_functions = types.Tool(
        function_declarations=[schema_get_files_info,
                               schema_get_file_content,
                               schema_write_file,
                               schema_run_python_file,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if response.function_calls:
        for fc in response.function_calls:

            tool_msg = call_function(fc, verbose=verbose)

            if not tool_msg.parts or not tool_msg.parts[0].function_response.response:
                raise RuntimeError("Function call did not return a response.")
            
            result_dict = tool_msg.parts[0].function_response.response

            if verbose:
                print(f"Function result: {result_dict}")

            messages.append(types.Content(role="tool", parts=tool_msg.parts))

    else:
        print(response.text)

    if verbose:
        """"
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        """
        print("Function calls:", fc.name , fc.args )

    
if __name__ == "__main__":
    main()



