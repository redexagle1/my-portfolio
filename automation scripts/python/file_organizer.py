#dependacies
import os # file manipulation
import glob # file searching
import argparse # command line enterface
import shutil # more file manipulation
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
    if validation_safety(old_dir):
        shutil.move(old_dir,new_dir)
        
def clear_empty_directories(dir):
    shutil.rmtree(dir)
    
def is_empty_dir(dir):
    assert os.listdir(dir) == []
     
def get_files_location(dir,*ext):
    file_type_dir_list = []
    for e in ext:
        file_type_dir_list.append(*glob.glob(f'{dir}/**/*.{e}', recursive = True ))
    return file_type_dir_list
def make_dir(dir,new_folder_name):
    os.chdir(dir)
    fold_path = os.path.join(dir,f'{new_folder_name}')
    os.mkdir(fold_path)
    return fold_path
def main():
    directory = get_input()
    directory = directory.replace('\\', '/')
    documents = ['pdf','doc','docm','docx','dot','dotx','txt','md']
    all_doc_dir =make_dir(directory,'documents')
    pdf_dir = make_dir(all_doc_dir,'pdf files')
    word_doc_dir = make_dir(all_doc_dir,'word doc files')
    txt_doc_dir = make_dir(all_doc_dir,'text files')
    markdown_doc_dir = make_dir(all_doc_dir,'markdown files')