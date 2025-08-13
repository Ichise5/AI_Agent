import os
from google.genai import types

#%% write_file function
def write_file(working_directory:str , file_path: str, content: str) -> str:

    # Get absolute paths
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Check if the target file path is in the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to  "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(abs_file_path,'w') as file:
            file.write(content)
    except Exception as e:
        return f'Error writing file "{file_path}": {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
# %%

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to the file in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write contents into, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents of the file to be written.",
            ),
        },
        required=["file_path", "content"],
    ),
)