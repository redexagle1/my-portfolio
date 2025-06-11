#dependacies
import os # file manipulation
import glob # file searching
import argparse # command line enterface
def validation_safety(file_path=""):
    """this function checks if the file has readonly property or not

    Args:
        file_path (str, optional): file_path. Defaults to "".

    Returns:
        boolean : returns False if it doesn't have the property 
                else returns True 
    """
    return False if os.access(file_path) else True

def get_input():
    """this function returns the input arguments from the command line

    Returns:
        str: your folder directory
    """
    parser = argparse.ArgumentParser(prog="file organizer" ,description="get the desired directory")
    parser.add_argument(
                        '--directory','-d',
                        type='str',
                        help="your desired directory"
                        )
    args = parser.parse_args()
    return args.directory

def move_files(old_dir,new_dir):
    ...
def clear_empty_directories(dir):
    ...
def is_empty_dir(dir):
    assert os.listdir(dir) == [] 
def get_files_location(dir,ext):
    ...
def main():
    directory = get_input()
