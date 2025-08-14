from google.genai import types
from functions.utils import get_validated_absolute_path


# %% write_file function
def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_file_path = get_validated_absolute_path(
            working_directory, file_path, is_dir=False
        )
    except ValueError as e:
        return str(e)

    try:
        with open(abs_file_path, "w") as file:
            file.write(content)
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'

    return (
        f'Successfully wrote to "{file_path}" ('
        f"{len(content)}"
        " characters written)"
    )


# %%

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Write contents to the file in the specified directory, "
        "constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the file to write contents into, "
                    "relative to the working directory."
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents of the file to be written.",
            ),
        },
        required=["file_path", "content"],
    ),
)
