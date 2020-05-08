#!/usr/bin/python3

import os
import sys
import shutil
import argparse
import pyperclip
import subprocess

# general settings
seperator_length = 40
default_username = 'No Name'
credential_file = os.path.expanduser('~/.cred')

# rofi keybindings
copy_username = 'Ctrl+C'
copy_password = 'Ctrl+c'
delete_credential = 'Ctrl+D'


class RofiException(Exception):
    '''
    Custom exception class. Not very useful :D
    '''


class DependencyException(Exception):
    '''
    Custom exception class. Not very useful :D
    '''


class Credential:
    '''
    This class represents a set of credentials (e.g. username and password).
    It can also be used to store usernames and password independent from each
    other. Furthermore, each credential can store a note (e.g. where the
    credential is used like ssh or website).
    '''
    filename = credential_file


    def __init__(self, username, password, note=''):
        '''
        Creates a new Credential object. If username is empty, the default
        username is used instead.

        Parameters:
            username        (string)            username of the credential.
            password        (string)            password of the credential.
            note            (string)            note about the credential.

        Returns:
            self            (Credential)        Credential object.
        '''
        self.note = note
        self.password = password

        if username == '':
            self.username = default_username
        else:
            self.username = username


    def __eq__(self, other):
        '''
        Two Credential objects are equal, if they share the same username,
        the same password and the same note.

        Parameters:
            self            (Credential)        copare object 1.
            other           (Credential)        copare object 2.

        Returns:
            boolean         (boolean)           True or False.
        '''
        bool1 = self.password == other.password
        bool2 = self.username == other.username
        bool3 = self.note == other.note
        return bool1 and bool2 and bool3


    def add(self):
        '''
        Add credential object to the credentials file. If the same combination
        of username, password and note already exists, do nothing.

        Parameters:
           self             (Credential)        credential object to add.

        Returns:
            None
        '''
        credentials = Credential.from_file()
        
        if self in credentials:
            return

        credentials.append(self)
        Credential.to_file(credentials)


    def from_file():
        '''
        Retrieve a list of stored credentials from the credential file.

        Parameters:
            None

        Returns:
            credential      (list)              list of Credential objects.
        '''
        if not os.path.isfile(Credential.filename):
            Credential.clean()

        with open(Credential.filename, 'r') as f:
            lines = f.readlines()

        credentials = []
        for i in range(0, len(lines), 3):
            username = lines[i].replace('\n', '')
            password = lines[i+1].replace('\n', '')
            note = lines[i+2].replace('\n', '')
            cred = Credential(username, password, note)
            credentials.append(cred)

        credentials.sort(key=lambda x: x.username.lower())
        return credentials


    def to_file(credentials):
        '''
        Takes a list of Credential objects and stores them to the credentials file.

        Parameters:
            credentials     (list)              list of Credential objects.

        Returns:
            None
        '''
        with open(Credential.filename, "w") as f:
            for credential in credentials:
                print(f'{credential.username}', file=f)
                print(f'{credential.password}', file=f)
                print(f'{credential.note}', file=f)


    def clean():
        '''
        Removes all entries from the credentials file. Can also be used to create
        the credentials file if not already present.
            
        Parameters:
            None

        Returns:
            None
        '''
        with open(Credential.filename, "w") as f:
            pass


    def start_rofi():
        '''
        Takes all credentials from the credentials file and displays them inside rofi.
        Depending on the key-combination pressed by the user, the function:

        * copies the selected username to the clipboard.
        * copies the selected password to the clipboard.
        * deletes the selected credential.

        Parameters:
            None

        Returns:
            None
        '''
        Credential.check_external_dependencies()

        credentials = Credential.from_file()
        key_mappings = ['-kb-custom-1', copy_password, '-kb-custom-2', copy_username, '-kb-custom-3', delete_credential]
        process = subprocess.Popen(['rofi', '-dmenu'] + key_mappings, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        for cred in credentials:
            spaces_note = (seperator_length - len(cred.password)) * ' '
            spaces_password= (seperator_length - len(cred.username)) * ' '
            process.stdin.write(f'{cred.username}{spaces_password}{cred.password}{spaces_note}{cred.note}\n'.encode('utf-8'))

        selection = (process.communicate()[0]).decode('utf-8')
        for cred in credentials:

            spaces_note = (seperator_length - len(cred.password)) * ' '
            spaces_password= (seperator_length - len(cred.username)) * ' '
            if selection == f'{cred.username}{spaces_password}{cred.password}{spaces_note}{cred.note}\n':
                
                # the exit code of rofi for -kb-custom-X is X+9.

                if process.returncode == 0 or process.returncode == 10:
                    pyperclip.copy(cred.password)
                    subprocess.call(['notify-send', '-t', '1500', f'{cred.password} copied to clipboard'])
                    return

                elif process.returncode == 11:
                    pyperclip.copy(cred.username)
                    subprocess.call(['notify-send', '-t', '1500', f'{cred.username} copied to clipboard'])
                    return

                elif process.returncode == 12:
                    credentials.remove(cred)
                    Credential.to_file(credentials)
                    Credential.start_rofi()
                    return

                else:
                    raise RofiException(f"start_rofi(..: rofi returned unexpected return code: {process.returncode}.")


    def check_external_dependencies():
        '''
        Checks if the required external execuatbles are present.

        Parameters:
            None

        Returns:
            None
        '''
        rofi = shutil.which('rofi')
        if not rofi:
            raise DependencyException("check_external_dependencies(..: cannot find 'rofi' in your current $PATH.")

        notify = shutil.which('notify-send')
        if not rofi:
            raise DependencyException("check_external_dependencies(..: cannot find 'notify-send' in your current $PATH.")



parser = argparse.ArgumentParser(description='''Simple credential manager for CTFs.''')
parser.add_argument('-u', '--user', dest='username', help='new username to store')
parser.add_argument('-p', '--password', dest='password', help='new password to store')
parser.add_argument('-n', '--note', dest='note', default='', help='note about the credential')
parser.add_argument('--clean', action='store_true', help='clear the credentials file')
args = parser.parse_args()


if args.clean:
    Credential.clean()
    sys.exit(0)

if args.username or args.password:
    username = args.username if args.username else ''
    password = args.password if args.password else ''
    cred = Credential(username, password, args.note)
    cred.add()
    sys.exit(0)

try:
    credential = Credential.start_rofi()
    sys.exit(0)
except Exception as e:
    print('[-] Exception was thrown: ' + str(e))
    sys.exit(1)
