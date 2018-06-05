# Data Analysis and Visualisation
This is the github repo of Anne Boomsma, Aram Elias, Tim Müller en Mirka Schoute, otherwise known as Group 27. All the files of their project can be found on this repo.

## Git init
To add this repository to your local git, simply run the following commands:
```
cd /path/to/git/folder
git init
git remote add origin git@github.com:aramelias/DAV.git
git pull origin master
```
A quick rundown of the commands:  
`cd /path/to/git/folder`  
This command moves the terminal to your desired folder. Replace `/path/to/git` with your own path.  
`git init`  
Initialises git in the folder.  
`git remote add origin git@github.com:aramelias/DAV.git`  
Tells git to add this repository to the list of repositories of chosen folder. This is what links git to your github.  
`git pull origin master`  
Download all files, testing your setup in the progress.

## SSH-key generation
Please note that is mandatory to have an SSH-key using this setup. If you do not have this, please run the following command:  
`ssh-keygen`  
This command first asks your for the path of your SSH key. Leave empty to use the default (~/.ssh/id_rsa). Then, it asks for a password to lock the file. Please leave empty to ease your life considerably. Afterwards, two files are created: ~/.ssh/id_rsa and ~/.ssh/id_rsa.pub (default location). Now run the following command:  
`cat ~/.ssh/id_rsa.pub`  
Again, the path used is that of the default location. Replace with your own if necessary. This command spits out the contents of the file in your terminal windows. Please make sure to copy all it's contents (including the final part that contains your email and / or your username).

Now that you have generated a key, add this to github. Simply go to your settings there, click on **SSH and GPG keys** and then **New SSH key**. Then, paste the contents of the file into the field and give the key a recognisable name. When done, save the key.

Now it's time to test your SSH key. Run this command:  
`ssh -T git@github.com`  
If you now see a welcoming message, congratiolations. Otherwise, make sure you ran all steps correctly and try again.
