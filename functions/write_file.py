from google.genai import types
from pathlib import Path


def write_file(working_directory, file_path, content):
    try:
        path_working_directory = Path(working_directory).resolve()
        target_path = (path_working_directory/file_path).resolve()

        try:
            target_path.relative_to(path_working_directory)
        except ValueError:
            return(f'Error: Cannot write to "{file_path}"'
                   ' as it is outside the permitted working directory.')
        
        try:
            target_path.touch(exist_ok=True)
            target_path.write_text(content)
            return(f"Succesfully wrote to '{file_path}'"
                   f" ({len(content)} characters written)")
        except Exception as e:
            return(f"Error: {e}")

    
    except Exception as e:
        return(f"Error: {e}")
    

schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Write or overwrite files to the specified file path, constrained within the working directory, using the specified content",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The file path to get the contents from, relative to the working directory."
			),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be writtent to the file path."
            ),
		},
	),
)