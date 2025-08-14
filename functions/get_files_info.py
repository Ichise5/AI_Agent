import os
from google.genai import types
from functions.utils import *
#from utils import get_validated_absolute_path

#%% get_files_info function
def get_files_info(working_directory: str, directory:str = ".") -> str:
    try:
        target_dir = get_validated_absolute_path(working_directory, directory, is_dir=True)
    except ValueError as e:
        return str(e)
    
    # Get information about the individual files and directories in the target directory
    try:
        files_info = []
        # scandir is faster than listdir
        for file in os.scandir(target_dir):
            stats = file.stat()
            files_info.append(
                f"- {file.name}: file_size={stats.st_size} bytes, is_dir={file.is_dir()}"
            )
        return "\n".join(files_info)
    # if file reading fails return an error
    except Exception as e:
        return f"Error listing files: {e}"
    
# %%

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
