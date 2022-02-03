import os


def check_presence_file(value_path:str) -> bool:
    """
    Function where we checked file presence
    Input:  value_path = path to the selected file
    Output: boolean value which shows presence of the file
    """
    return os.path.exists(value_path) and not os.path.isdir(value_path)

def check_presence_directory(value_path:str) -> bool:
    """
    Function where we checked folder presence
    Input:  value_path = path to the selected folder
    Output: boolean value which shows presence of the folder
    """
    return not os.path.exists(value_path) and not os.path.isfile(value_path)

def create_directory(value_path:str) -> None:
    """
    Function where we check and create the values
    Input:  value_path = path to the directory
    Output: we developed 
    """
    os.path.exists(value_path) or os.mkdir(value_path)