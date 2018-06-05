# Data Analysis and Visualisation
This is the github repo of Anne Boomsma, Aram Elias, Tim Müller en Mirka Schoute, otherwise known as Group 27. All the files of their project can be found on this repo.

## Git setup
### SSH-key generation
Please note that is mandatory to have an SSH-key using this setup. If you do not have this, please run the following command:  
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
Replace `your_email@example.com` by the email you used to create your github account. This command first asks your for the path of your SSH key. Leave empty to use the default (~/.ssh/id_rsa). Then, it asks for a password to lock the file. Please leave empty to ease your life considerably. Afterwards, two files are created: ~/.ssh/id_rsa and ~/.ssh/id_rsa.pub (default location). Now run the following command:  
```
cat ~/.ssh/id_rsa.pub
```
Again, the path used is that of the default location. Replace with your own if necessary. This command spits out the contents of the file in your terminal windows. Please make sure to copy all it's contents (including the final part that contains your email and / or your username).

Now that you have generated a key, add this to github. Simply go to your settings there, click on **SSH and GPG keys** and then **New SSH key**. Then, paste the contents of the file into the field and give the key a recognisable name. When done, save the key.

Now it's time to test your SSH key. Run this command:  
```
ssh -T git@github.com
```
If you now see a welcoming message, you've successfully setup your SSH key and you're done. Otherwise, make sure you added the key to your ssh agent:  
First, run:  
```
eval "$(ssh-agent -s)"
```
This starts the SSH agent in the background. Then, run the following command to add it:  
```
ssh-add ~/.ssh/id_rsa
```  
Again, replace this path to your own if you used a custom path. In either case, please make sure you have actually generated a SSH key in the file you're pointing to.

### Git init
To add this repository to your local git, simply run the following commands:
```
cd /path/to/git/folder
git clone git@github.com:aramelias/DAV.git
```
A quick rundown of the commands:  
`cd /path/to/git/folder`  
This command moves the terminal to your desired folder. Replace `/path/to/git` with your own path.  
`git clone git@github.com:aramelias/DAV.git`  
Clones the git repository into your designated folder. When done, your git should be setup properly. Do note that this will add the repo to a sub-folder in your current folder, named 'DAV'.

## Git usage
Using git through the command line is simple. Here's how to use it:
### Pulling
To pull files from git, use the following command:  
```
git pull origin master
```
Replace `master` if necessary by another branch.
### Pushing
Pushing to the git repository is slightly more complicated. This requires three commands to be run:  
```
git add .
```
This adds all git files to the list of files that you want to upload. Replace `.` with a specific file name to only add that file to the upload. You can repeat this process to add all the files you want.  
```
git commit -m "Enter your message here"
```
This computes which files should be updated because they're changed and which not. The bit following the `-m` is the message, which is a very brief explaination of what you did. An example message would be: **"Updated README.md"**.  
```
git push origin master
```
Finally, use this command to push all changed files to the server.
