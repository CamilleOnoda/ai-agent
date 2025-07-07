from pathlib import Path
import sys


def get_files_info(working_directory, directory=None):
    try:
        path_working_directory = Path(working_directory)
        if directory != None:
            path_directory = Path(directory)
            full_path = Path(f"{working_directory}/{directory}/")
            list_content_workingDir = list(path_working_directory.glob("*"))
            list_item_workingDir = [content.name for content in list_content_workingDir]
            list_content_fullPath = list(full_path.glob("*"))

            if directory == "." or directory == "":
                list_item_workingDir.append(directory)

            if directory not in list_item_workingDir:
                    print(f'Error: Cannot list "{directory}"'
                    ' as it is outside the permitted working directory')
                    sys.exit(0)
            elif not full_path.is_dir():
                print(f'Error: "{directory}" is not a directory')
            else:
                if path_directory.name != "":
                    print(f"Result for '{directory}' directory:")
                else:
                    print("Result for current directory:")
                for content in list_content_fullPath:
                    file_size = content.stat().st_size
                    if content.is_dir():
                        print(f"- {content.name}: file_size={file_size} bytes, is_dir=True")
                    else:
                        print(f"- {content.name}: file_size={file_size} bytes, is_dir=False")

    except Exception as e:
        print(f"Error: {e}")

