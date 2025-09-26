import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(file_path)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_path)

    if args is None:
        args = []

    if not abs_target.startswith(abs_target):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    subprocess_args = ["python3", full_path] + args

    try:
        completed = subprocess.run(
        subprocess_args, timeout=30,
        capture_output=True,
        text=True,
        cwd=working_directory
    )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = []
    output.append("STDOUT:")
    output.append(completed.stdout or "")
    output.append("STDERR:")
    output.append(completed.stderr or "")

    if completed.returncode != 0:
        output.append(f"Process exited with code X")

    if completed.stdout.strip() == "" and completed.stderr.strip() == "":
        output.append("No output produced.")

    result = "\n".join(output)
    return result

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Excutes a specified Python file within the working directory and captures its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path of the Python file to execute within the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of command-line arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)






