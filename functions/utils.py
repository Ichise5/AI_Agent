import os

def get_validated_absolute_path(working_directory: str, file_path: str, is_dir: bool) -> str:
    """
    Validates a relative path and converts it to an absolute path within the working directory.
    Raises ValueError if the path is outside the working directory.
    """
    abs_working_dir = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    # Ensure the path is within the working directory
    if not abs_path.startswith(abs_working_dir):
        raise ValueError(f"Attempted to access path outside working directory: {file_path}")

    # Basic check for existence and type (file/directory)
    if is_dir and not os.path.isdir(abs_path):
        raise ValueError(f"Path is not a directory: {file_path}")
    elif not is_dir and not os.path.isfile(abs_path):
        # For files, it's okay if it doesn't exist yet for write operations
        # But for read operations, it should exist. This function doesn't
        # distinguish, so a basic check is fine.
        pass # Will be handled by open() in calling functions for files

    return abs_path
