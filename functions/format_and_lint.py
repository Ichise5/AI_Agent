import subprocess
from google.genai import types
from functions.utils import get_validated_absolute_path


def format_and_lint_file(working_directory: str, file_path: str) -> dict:
    """Formats and lints a Python file using Black and Flake8.

    Args:
        working_directory: The current working directory.
        file_path: The path to the Python file to format and lint, relative to the working directory.

    Returns:
        A dictionary indicating the success or failure of the operations, along with any output.
    """
    try:
        abs_file_path = get_validated_absolute_path(
            working_directory, file_path, is_dir=False
        )
    except ValueError as e:
        return {"error": str(e)}

    # Run Black formatting
    try:
        black_result = subprocess.run(
            ["black", abs_file_path], capture_output=True, text=True, check=True
        )
        black_output = {
            "message": f"Black formatting successful for {file_path}",
            "stdout": black_result.stdout,
            "stderr": black_result.stderr,
        }
    except subprocess.CalledProcessError as e:
        return {
            "error": f"Error during Black formatting for {file_path}",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "return_code": e.returncode,
        }
    except FileNotFoundError:
        return {
            "error": "Black is not installed or not found in PATH. Please install Black using 'pip install black'"
        }

    # Run Flake8 linting
    try:
        flake8_result = subprocess.run(
            ["flake8", abs_file_path], capture_output=True, text=True, check=True
        )
        flake8_output = {
            "message": f"Flake8 linting successful for {file_path}",
            "stdout": flake8_result.stdout,
            "stderr": flake8_result.stderr,
        }
    except subprocess.CalledProcessError as e:
        return {
            "error": f"Flake8 linting failed for {file_path}",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "return_code": e.returncode,
        }
    except FileNotFoundError:
        return {
            "error": "Flake8 is not installed or not found in PATH. Please install Flake8 using 'pip install flake8'"
        }

    return {
        "result": "Formatting and linting completed.",
        "black_output": black_output,
        "flake8_output": flake8_output,
    }


schema_format_and_lint = types.FunctionDeclaration(
    name="format_and_lint_file",
    description="Formats and lints a Python file using Black and Flake8.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The current working directory.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to format and lint, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
