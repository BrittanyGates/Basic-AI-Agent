from google.genai import types
import os
import subprocess

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified Python function, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python script.",
            ),
        },
        required=["file_path"],
    ),
)


def run_python_file(working_directory: str, file_path: str, args=[]):
    full_path = os.path.join(working_directory, file_path)
    absolute_full_path = os.path.abspath(full_path)
    absolute_working_dir = os.path.abspath(working_directory)

    # Boundary check
    if not (absolute_full_path == absolute_working_dir or absolute_full_path.startswith(absolute_working_dir + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # File check
    if not os.path.exists(absolute_full_path):
        return f'Error: File "{file_path}" not found.'

    # File extension check
    if not absolute_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = subprocess.run(["python", absolute_full_path] + args, cwd=absolute_working_dir, capture_output=True, text=True, timeout=30)
        stdout = result.stdout
        stderr = result.stderr
        result_exit_code = result.returncode
        result_parts = []

        if stdout:
            result_parts.append(f"STDOUT: {stdout}")

        if stderr:
            result_parts.append(f"STDERR: {stderr}")

        if result_exit_code != 0:
            result_parts.append(f"Process exited with code {result.returncode}")

        if not result_parts:
            return "No output produced."
        return "\n".join(result_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"


