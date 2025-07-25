from pathlib import Path
from functions.config import CHAR_LIMIT
from google.genai import types


def get_file_content(working_directory, file_path):
	try:
		path_working_directory = Path(working_directory).resolve()
		target_path = (path_working_directory / file_path).resolve()

		try:
			target_path.relative_to(path_working_directory)
		except ValueError:
			return(f'Cannot read "{file_path}"'
				   ' as it is outside the permitted working directory')
			
		if not target_path.is_file():
			return(f'Error: File not found or is not a regular file: "{file_path}"')
		
		try:
			with target_path.open("r", encoding="utf-8") as file:
				content = file.read()
			character_count = len(content)
			if character_count > CHAR_LIMIT:
				return f'{content[:CHAR_LIMIT]}\n[...File "{file_path}" truncated at 10_000 characters]'
			else:
				return target_path.read_text()
		except Exception as e:
			return f"Error reading {file_path}: {e}"
			
	except Exception as e:
		return(f"Error: {e}")


schema_get_file_content = types.FunctionDeclaration(
	name="get_file_content",
	description="Get the contents of a file in the specified directory, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The file path to get the contents from, relative to the working directory."
			),
		},
	),
)