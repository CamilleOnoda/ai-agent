from pathlib import Path


def get_file_content(working_directory, file_path):
    try:
        path_working_directory = Path(working_directory).resolve()
        target_path = (path_working_directory / file_path).resolve()

        try:
            target_path.relative_to(path_working_directory)
        except ValueError:
            return(f"Cannot read '{file_path}'" 
                   " as it is outside the permitted working directory")
            
        if not target_path.is_file():
            return(f"Error: File not found or is not a regular file: '{file_path}'")

    except Exception as e:
        return(f"Error: {e}")


get_file_content("calculator", "etc")