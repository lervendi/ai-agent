import os
from google import genai
from google.genai import types


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_path)

    if not abs_target.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: The directory "{directory}" is not a directory'
    
    try:
        lines = []
        for name in os.listdir(full_path):
            path = os.path.join(full_path, name)
            is_dir = os.path.isdir(path)
            size = os.path.getsize(path)
            line = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            lines.append(line)
    except Exception as e:
        return f"Error: {e}"
    
    return "\n".join(lines)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)