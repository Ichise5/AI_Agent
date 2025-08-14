import os
from google.genai import types
from functions.utils import *


# %% delete_file function
def delete_file(working_directory: str, file_path: str) -> str:
    """Deletes a file in the specified directory.

    Args:
        file_path (str): The path to the file to be deleted, relative to the working directory.

    Returns:
        str: A message indicating the success or failure of the deletion.
    """
    try:
        target_file = get_validated_absolute_path(
            working_directory, file_path, is_dir=False
        )
    except ValueError as e:
        return str(e)

    try:
        os.remove(target_file)
        return f"File '{file_path}' deleted successfully."
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"Error deleting file '{file_path}': {e}"


# %%
schema_delete_file = types.FunctionDeclaration(
    name="delete_file",
    description="Deletes a file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be deleted, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
