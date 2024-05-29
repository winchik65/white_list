#---The "White List" program---
#Is a tool for encrypting files and folders using cryptographic keys
#---whitelist crypt 2---
#by winchik65
import getopt, sys, os, glob

from cryptography.fernet import Fernet

def create_key():
    key = Fernet.generate_key()
    with open('kluch.key', 'wb') as filekey:
        filekey.write(key)
    return key

def get_key():
    key = None
    if os.path.isfile('kluch.key'):
        with open('kluch.key', 'rb') as key_file:
            key = key_file.read()
    else:
        key = create_key()
    
    return Fernet(key)


def encrypt(file_name):
    if file_name == '' or os.path.isdir(file_name):
        ecrypt_folder(file_name)
    else:
        encrypt_file(file_name)

def encrypt_file(file_name, key):
    fernet = key
    with open(file_name, 'rb') as file:
        original = file.read()
    enc = fernet.encrypt(original)
    with open(file_name, 'wb') as enc_file:
        enc_file.write(enc)
    
    print(f'file {file_name} is encrypted')

#encrypt all files in a specified folder
def ecrypt_folder(folder_name):
    key = get_key()
    if(folder_name == ''):
        path = os.path.join(os.getcwd(), '**/*.*')  #Create a path to files in the current directory
    else:
        path = os.path.join(folder_name, '**/*.*')
        
    for file in glob.glob(path, recursive=True):
        encrypt_file(file, key)
        

def list_files(dir_name):
    for file in glob.glob(os.path.join(dir_name, '**/*.*'), recursive=True):
        print(file)


def decrypt(file_name):
    if file_name == '' or os.path.isdir(file_name):
        decrypt_folder(file_name)
    else:
        decrypt_file(file_name)

def decrypt_file(file_name):
    if not (".db" in file_name) and not ("~$" in file_name) :
        fernet = get_key()
        with open(file_name, 'rb') as file:
            original = file.read()
        enc = fernet.decrypt(original)
        with open(file_name, 'wb') as enc_file:
            enc_file.write(enc)
        
        print(f'file {file_name} is decrypted')

def decrypt_folder(folder_name):
    key = get_key()
    if(folder_name == ''):
        path = os.path.join(os.getcwd(), '**/*.*')
    else:
        path = os.path.join(folder_name, '**/*.*')
        
    for file in glob.glob(path, recursive=True):
        decrypt_file(file)

def help_info():
    print("""
        The White List help manual
        -For encrypt: 
                      whitelist -e <folder_path>
                      whitelist --Encrypt <folder_path>
        -For decrypt: 
                      whitelist -d <folder_path>
                      whitelist --Decrypt <folder_path>
        -List files in folder:
                      whitelist -l <folder_path>
                      whitelist --List <folder_path>
        -Echo test:
                      whitelist -t message
                      whitelist --Test message
          """)


def main(args):
    for arg, val in args:
        if arg in ('-t', '--Test'):
            print(f'it is test ... {sys.argv[2]}')
        elif arg in('-e', '--Encrypt'):
            encrypt(sys.argv[2])
        elif arg in ('-d', '--Decrypt'):
            decrypt(sys.argv[2])
        elif arg in ('-l', '--List'):
            list_files(sys.argv[2])
        elif arg in ('-h' '--Help'):
            help_info()


if __name__ == '__main__':
    long_options = ["List", "Test", "Create_key", "Decrypt", "Encrypt", "Help"]
    options = "hltcde:"
    args = sys.argv[1:]
    arguments, values = getopt.getopt(args, options, long_options)
    if len(arguments) > 1:
        print('to many arguments...')
    main(arguments)