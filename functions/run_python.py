import os
import subprocess
from google.genai import types

#%% run_python_file function
def run_python_file(working_directory: str, file_path: str, args=[]) -> str:
    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the target file path is in the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith("py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", abs_file_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

    except Exception as e:
        f"Error: executing Python file: {e}"

    if output:
        return "\n".join(output)
    else:
        return "No output produced."

# %%
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run pythonic file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be run, relative to the working directory.",
            ),
          "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)