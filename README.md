## CTF Credential Manager

----

During *CTFs* it is common to obtain several usernames and passwords.
Just storing these inside of text files becomes confusing very quickly
and accessing them is also not really fast. This tool is designed to
allow fast, organized and simple access to *CTF* credentials.

![example](/resources/example.gif)


### Installation

----

The tool itself requires no installation, as it is a simple standalone python script.
However, a few external requirements should be met:

* **rofi**: used for displaying credentials. On most distributions, this took can be installed
  using a package manager:
  ```
  $ sudo apt install rofi         # Debian
  $ pacman -S rofi                # Arch
  ```

* **libnotify** and a **notification server**: These are shipped per default on most
  distributions. Just type ``$ notify-send test`` to check if they are available.
  If not, read about [desktop notifications](https://wiki.archlinux.org/index.php/Desktop_notifications)
  and decide if you want to install them. You can also strip calls to **notify-send**
  from the code, if you don't want desktop notifications.

* **pyperclip**: If I'm not mistaken, this should be the only python dependency
  that you have to install manually. Just run:
  ```
  $ pip3 install pyperclip --user         # or ...
  $ pip3 install -r requirements.txt      # from the repository folder
  ```


### Usage

----

It is recommended to configure the script with a short and simple name (e.g. ``cred``) 
inside your default ``$PATH``. After it is configured, you can store a new set of credentials
using the following command:

```
$ cred -u example -p '$3cReTp@55w0rD!'
$ cat ~/.cred
example
$3cReTp@55w0rD!

```

As you can see, the credentials have been saved in plaintext to the file ``~/.cred``.
You can also store only usernames or only passwords like this:

```
$ cred -u example2
$ cred -p 'NewPassword:)'
$ cat ~/.cred
example
$3cReTp@55w0rD!

example2


No Name
NewPassword:)

```

Furthermore, a note can be assigned to each credential like this:

```
$ cred -u user1 -p 's3crEt' -n 'mysql'
$ cat ~/.cred
example
$3cReTp@55w0rD!

example2


No Name
NewPassword:)

user1
s3crEt
mysql
```

From the output above, you might already guessed that credentials are stored
in a ``<username>\n<password>\n<note>\n`` format. If no username is supplied, the default username
``No Name`` is chosen. You can modify this default username in the first few lines of the
script.

To obtain stored credentials from the credentials file, simply run the script without any
arguments. After launching it, *rofi* should pop up and present you a list of available credentials.
The following keybindings apply to *rofi* (can be modified in the first few lines of the script):

* ``ctrl+c`` or ``Enter``: copy the selected password to the clipboard.
* ``ctrl+Shift+c``: copy the selected username to the clipboard.
* ``ctrl+Shift+d``: delete the selected credential.

It is recommended to bind this form of script execution to a shortcut. E.g. then using
*i3 window manager*, you can use the following configuration:

```
bindsym $mod+p --release exec --no-startup-id cred
```


### Warning

----

This tool should not be used to store any sensitive information like private usernames or passwords.
As mentioned above, all entered credentials are saved as plaintext on your disk. This behavior is insecure
and should only be used to store non sensitive data, like credentials obtained during a *CTF*.
