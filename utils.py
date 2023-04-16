
def read_release_note(file_path):
    """
    Reads the content of a file and returns the file content as a string.

    Args:
        file_path (str): The file path of the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except Exception as e:
        print(f'Error reading release note path: {str(e)}')
        raise
