from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)


def call_function(function_call_part, verbose=False):

    function_name = function_call_part.name
    function_args = dict(function_call_part.args or {})

    if verbose:
        print(f"Calling function: {function_name}({function_args})")

    else:
        print(f" - Calling function: {function_name}")

    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name not in functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_name,
                responce={"error": f"Unknown function: {function_name}"},
                )
            ]
        )
    
    function_args["working_directory"] = "./calculator"

    function_result = functions[function_name](**function_args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ]
    )
    
