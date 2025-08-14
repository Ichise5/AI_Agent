import subprocess
import sys


def run_black_formatter(file_path):
    try:
        result = subprocess.run(
            ["black", file_path], capture_output=True, text=True, check=True
        )
        print(f"Black formatting successful for {file_path}")
        print(result.stdout)
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error during Black formatting for {file_path}:")
        print(e.stdout)
        print(e.stderr)
        sys.exit(e.returncode)
    except FileNotFoundError:
        print("Error: Black is not installed or not found in PATH.")
        print("Please install Black using 'pip install black'")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_to_format = sys.argv[1]
        run_black_formatter(file_to_format)
    else:
        print("Usage: python black_formatter.py <file_path>")
        sys.exit(1)
