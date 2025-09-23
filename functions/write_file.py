import os 

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(full_path)

    if not abs_target.startswith(abs_working):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)
            
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
