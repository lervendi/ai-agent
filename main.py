import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import call_function, available_functions
from config import MAX_STEPS


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

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    
    for _ in range(MAX_STEPS):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt, #*system prompt
                ),
            )

            for cand in (response.candidates or []):
                if cand and cand.content:
                    messages.append(cand.content)

            function_calls = list(response.function_calls or [])

            if function_calls:
                for fc in function_calls:
                    if verbose:
                        print(f"Model decided to call function: {fc.name} with args {dict(fc.args or {})}")
                    try:
                        tool_msg = call_function(fc, verbose=verbose)  # role="tool"
                        
                        messages.append(types.Content(role="user", parts=tool_msg.parts))
                    except Exception as e:
                        err_msg = types.Content(
                            role="tool",
                            parts=[types.Part.from_function_response(
                                name=fc.name,
                                response={"error": f"Exception during function call: {e}"},
                            )]
                        )
                        messages.append(types.Content(role="user", parts=err_msg.parts))
                
                continue


            final_text = (response.text or "").strip()
            if verbose:
                print(f"\nModel response text: {final_text}\n")

            if final_text:
                print(final_text)
                break

        except Exception as e:
            print(f"Error during agent loop: {e}")
            break

    else:
        print("Error: Maximum steps reached without a final answer.")

if __name__ == "__main__":
    main()