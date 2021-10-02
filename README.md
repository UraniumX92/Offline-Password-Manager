# Offline Password Manager 

**Version : 1.0**

## About :
This is an offline Password Manager, which encrypts the passwords and stores it in the `.json` files and retrieves
the passwords and decrypts the encrypted password, and shows to user.
> **Note :** `.json` files are automatically generated when the program starts for the first time.
 
>***
## Encryption :
The Encryption done to protect the passwords from being readable by someone who opens the `.json` file is similar to that of [Encryptor I made](https://github.com/UraniumX92/Encryptor "Link to the GitHub Repository of Encryptor that I made.") a few days ago from now.

The Key is randomly generated and stored in a `.json` file.

But only the program knows how to handle and use the key. Because the key visible in `.json` file is not the actual key.

Even if someone uses the key from `.json` file, They wouldn't be able to extract the passwords. As the key visible is not the actual key.

>***
## Features :
***
* **Show Passwords :**
  * Shows the list of passwords, select a password to get it displayed in an Entry widget. Initially the password is not shown in plain text, rather bullet characters `•` are shown.
    * There are 2 buttons beside the Entry widget.
    * 1.Show / Hide
      * When bullet characters are shown in the entry, pressing this button will show the password in plain text and vice versa.
    * 2.Copy
      * If you just want to copy the password (even without looking at password in plain text), press this button to copy password to your clipboard, and the button text will change from 'Copy' to 'Copied'
***        
* **Add a New Password :**
  * Want to add a new Platform and password, this is your option to go. just simple enter and submit to add the password.
***
* **Change Existing Passwords :**
  * If you changed a Platform's password online, and you want to change in this app too, choose this option.
    * Same layout as in 'Show Passwords' option.
    * But here you can interact with the password Entry widget and change the password in it and press the 'Change Selected Password' button and then password will be changed.
***
* **Remove Existing Platform-Password Pair :**
  * If you want to remove a platform-password pair from the data, select this option.
>***

> ***IMPORTANT NOTE :*** **The one and only password you have to remember is, your Master Password, If you forget your Master Password, there is no way to retrieve it back (yet) as this is an Offline Manager.**
>
> **Though you can change your Master Password from the Login screen, from when you open the app for 2nd time after initial setup. and to do that, you will be prompted to enter your current Master Password first.**