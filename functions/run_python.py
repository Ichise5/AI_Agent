import os
import subprocess
from google.genai import types
from functions.utils import get_validated_absolute_path


# %% run_python_file function
def run_python_file(working_directory: str, file_path: str, args=[]) -> str:
    try:
        abs_file_path = get_validated_absolute_path(
            working_directory, file_path, is_dir=False
        )
    except ValueError as e:
        return str(e)

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
            cwd=os.path.abspath(working_directory),
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
