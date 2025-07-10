from pathlib import Path
from google import genai
from google.genai import types
            

def get_files_info(working_directory, directory=None):
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


    try:
        path_working_directory = Path(working_directory).resolve()
        if directory is None:
            target_path = path_working_directory
        else:
            target_path = (path_working_directory / directory).resolve()

        list_content_target_path = list(target_path.glob("*"))

        try:
            target_path.relative_to(path_working_directory)
        except ValueError:
            return(f'Error: Cannot list "{directory}"'
                ' as it is outside the permitted working directory')
        
        if not target_path.is_dir():
            return(f'Error: "{directory}" is not a directory')
        else:
            lines = []
            for content in list_content_target_path:
                file_size = content.stat().st_size
                is_dir = content.is_dir()
                lines.append(f"- {content.name}: file_size={file_size} bytes, is_dir={is_dir}")
            description = "\n".join(lines)
            
            if directory is None or directory == ".":
                header = "Result for current directory:"
            else:
                header = f"Result for {directory} directory:"
            return f"{header}\n{description}"
        
    except Exception as e:
        return(f"Error: {e}")
    

