# Understanding Your Working Environment

In Linux, each user typically has a "home directory," represented by ~. However, in this lab environment, we'll start in the /home/labex/project directory, which is our default working directory.

```pwd```

pwd stands for "print working directory". It displays your current location in the file system. This command is crucial for orienting yourself in the Linux file structure. You should see /home/labex/project as the output.

Now, let's explore the relationship between the current directory and the home directory:

```
echo ~
```
Note: If you cannot type the ~ symbol in the Desktop terminal due to keyboard layout differences in certain countries, you can try switching to the standalone Terminal tab in the upper left corner of the VM interface.

This command will display the path to your home directory, which should be /home/labex.

To see the contents of your current directory, use:

```
ls
```
Let's also check the contents of your home directory:

```
ls ~
```
This command lists the contents of your home directory, which may be different from your current working directory.

Understanding the distinction between your current working directory and your home directory is important for navigating the Linux file system effectively.

---
# Navigating the File System

Linux uses what we call a "hierarchical file system". Think of it like a big tree with branches. The main trunk is called the "root directory", represented by a single forward slash /. All other directories and files branch out from this root.

Let's explore how to move around in this tree-like structure:

    Check your current location:

```
pwd
```

This should show /home/labex/project. If it doesn't, you might be in a different directory. Use cd /home/labex/project to get back to the starting point.

    View the contents of your current directory:

```
ls
```

This lists all files and folders in your current location. /home/labex/project is empty, so you won't see anything.

    Move up one level to the parent directory:

```
cd ..
```

The .. means "the directory above". After this command, do pwd again. You should now be in /home/labex.

-    Return to your project directory:

```
cd project
```

This takes you back to /home/labex/project.

-     Go to your home directory:

```
cd ~
```

The ~ is a shortcut for your home directory. Do pwd to confirm you're in /home/labex.

-     Return to the project directory using an absolute path:

```
cd /home/labex/project
```

This is called an "absolute path" because it starts from the root (/) and gives the full location.

--- 

# Creating Files and Listing Directory Contents

Now that we know how to navigate, let's create some files and explore how to list directory contents.

First, make sure you're in the /home/labex/project directory:

```
cd /home/labex/project
```


Let's create a few files:

```
touch file1.txt
```
The touch command is used to create an empty file. If the file already exists, it updates the file's timestamp without changing its content. It's a simple way to create new, empty files.

```
echo "Hello, Linux" > file2.txt
```

This command does two things:

 echo is a command that prints text.
The > symbol redirects the output of echo into a file named file2.txt. If the file doesn't exist, it's created. If it does exist, its content is replaced.

```
echo "Hidden file" > .hiddenfile
```

This creates a hidden file. In Linux, any file or directory name that starts with a dot (.) is considered hidden.

Now, let's create a directory:
```
mkdir testdir
```
The mkdir command (short for "make directory") creates a new directory named testdir.

Basic listing:
```
ls
```
- Directory contents listing output

This shows the contents of your current directory. You should see file1.txt, file2.txt, and testdir.

Detailed listing:
```
ls -l
```
The -l option (that's a lowercase L, not the number 1) provides a "long" format listing. You'll see additional details like file permissions, owner, size, and modification date.

Show hidden files:
```
ls -a
```
This will show all files, including the hidden .hiddenfile we created.

Combine options:
```
ls -la
```
This combines the long format (-l) with showing all files (-a).

List contents of a specific directory:
```
ls -l testdir
```
This lists the contents of the testdir directory (which should be empty at this point).

---

# Copying Files and Directories

Now that we have some files to work with, let's learn how to copy them:

    Copy a file:
```
cp file1.txt file1_copy.txt
```

This creates a copy of file1.txt named file1_copy.txt in the current directory.

Let's verify the copy:
```
ls
```
Copy a file to another directory:
```
cp file2.txt testdir/
```
This copies file2.txt into the testdir directory.
 
Copy a directory:
```
cp -r testdir testdir_copy
```
The -r option stands for "recursive". It's necessary when copying directories to ensure all contents are copied.

Verify our copies:
```
ls
ls testdir
ls testdir_copy
```


--- 

# Moving and Renaming Files and Directories

The mv command is used for both moving and renaming in Linux:

Rename a file:
```
mv file1.txt newname.txt
```

This renames file1.txt to newname.txt.

Move a file to a directory:
```
mv newname.txt testdir/
```
This moves newname.txt into the testdir directory.

Rename a directory:
```
mv testdir_copy new_testdir
```
This renames testdir_copy to new_testdir.

Move and rename in one command:
```
mv testdir/newname.txt ./original_file1.txt
```
This moves newname.txt out of testdir and renames it to original_file1.txt in the current directory.

Verify our changes:
```
ls
ls testdir
```

---

# Removing Files and Directories

Removing files and directories is a powerful operation. Unlike graphical interfaces, the command line often doesn't have a "Recycle Bin" or "Trash". Deletions made with rm are usually permanent. Always double-check your commands before executing them!

Let's clean up the files and directories we created. Make sure you are in the /home/labex/project directory.

```
pwd
ls -a
```

You should see files like original_file1.txt, .hiddenfile, file2.txt, and directories like testdir, new_testdir.

```
-rw-rw-r-- 1 labex labex   12 May  3 08:44 .hiddenfile
-rw-rw-r-- 1 labex labex    0 May  3 08:45 file1_copy.txt
-rw-rw-r-- 1 labex labex   13 May  3 08:44 file2.txt
drwxrwxr-x 2 labex labex   23 May  3 08:45 new_testdir
-rw-rw-r-- 1 labex labex    0 May  3 08:44 original_file1.txt
drwxrwxr-x 2 labex labex   23 May  3 08:45 testdir
```
Remove a single file:
```
    rm original_file1.txt
```
The rm command (short for "remove") deletes files. Let's check:
```
    ls
```
original_file1.txt should be gone.

Remove interactively (safer):

Let's try to remove file2.txt, but this time using the interactive flag -i:
```
    rm -i file2.txt
```
The -i option prompts you for confirmation before deleting each file. Type y (for yes) and press Enter to confirm the deletion. If you type n or anything else, the file will not be deleted.
`` 
    ls
`` 
If you confirmed, file2.txt will be gone.

Remove an empty directory:

Remember the new_testdir we created by renaming testdir_copy? Let's check if it's empty:
```
    ls new_testdir
```
If it's empty (shows no files), we can remove it using rmdir:
```
    rmdir new_testdir
```
rmdir (remove directory) only works on empty directories.
`` 
    ls
`` 
new_testdir can't be removed because it's not empty.

Attempt to remove a non-empty directory:

Now, let's try rmdir on testdir, which still contains file2.txt (copied in Step 4):
`` 
    ls testdir
    rmdir testdir
```
You will likely see an error message like rmdir: failed to remove 'testdir': Directory not empty. This is expected because rmdir cannot remove directories that contain files or other directories.

Remove a directory and its contents (recursively):

To remove a directory that is not empty, we need to use rm with the -r (recursive) option:
```
    rm -r testdir
```
This command removes the testdir directory and everything inside it. Use this command with caution.
```
    ls
```
testdir should now be gone.

Force removal (use with extreme caution):

Sometimes, you might want to remove files without being prompted, even if they are write-protected (though we don't have any here). The -f (force) option does this.

Let's remove our hidden file:
```
    rm .hiddenfile
    ls -a
```
Now, let's combine -r and -f. The rm -rf command is extremely powerful and potentially dangerous. It removes directories recursively (-r) and forces removal without prompting (-f).

!!! DANGER ZONE !!!
Be ABSOLUTELY SURE you know what you are deleting before running rm -rf. A small typo could delete critical system files or your personal data. There is no undo. For example, rm -rf / could attempt to delete your entire system (if you have permissions). Always double-check the path.

Let's create a temporary directory and file to demonstrate (safely):
```
    mkdir temp_dir
    touch temp_dir/temp_file.txt
    ls -R temp_dir
```
Note: You might notice we used -R (uppercase) with ls instead of -r (lowercase) like we did with cp and rm. This is not just a case difference - they are completely different options! For ls, -R means "recursive listing" (list subdirectories), while -r means "reverse sort order". For cp and rm, the recursive option is -r (lowercase). Always check the manual (man command) to understand each command's specific options.

Now, let's remove it forcefully:
```
    rm -rf temp_dir
```
Verify the removal:
```
```
ls
```

temp_dir should be gone.

Remember: In Linux command line, deleted files are generally gone forever. Use rm carefully!.


## Summary

Congratulations! You've learned the essential file operations in Linux:

Navigating the file system with cd and pwd
    Creating files and directories with touch and mkdir
    Listing contents with ls and its options
    Copying files and directories with cp
    Moving and renaming with mv
    Removing files and directories with rm and rmdir

These commands form the foundation of file management in Linux. With practice, you'll become proficient in managing your files and directories from the command line.

Remember to use these commands carefully, especially rm, as it permanently deletes files and directories without the possibility of recovery.

As you continue your Linux journey, explore man pages (e.g., man ls) to learn more about each command and its options. Happy exploring!

--- 



# Print File Contents

First, please open a terminal on the Desktop OR switch to the terminal tab in the lab environment.

Once you have a terminal open, you should see a command prompt, typically ending with a $ symbol. This is where we'll enter our commands.

Now, let's use the cat command to display the contents of a file:

In the terminal, type the following command and press Enter:

```
cat /tmp/hello
```

Here, /tmp/hello is the path to the file we want to view. /tmp is a directory (folder) on your system, and hello is the name of the file in that directory.

After pressing Enter, you should see the contents of the file:

```
Hi,
I am Labby!
```

This is everything that's in the /tmp/hello file. The cat command has displayed it for us in the terminal.

--- 

# Display File Contents with Line Numbers

Now, let's use the cat command again, but this time we'll add line numbers to the output.

In the terminal, type the following command and press Enter:
```
cat -n /tmp/hello
```
The -n here is called an option or a flag. It tells cat to number all output lines.

You should now see the contents of the file with line numbers:
```
     1 Hi,
     2 I am Labby!
```
This can be very helpful when you're dealing with longer files and need to refer to specific lines.

---

# Print the Top Lines of a File

Next, we'll use the head command. As its name suggests, head is used to view the beginning or "head" of a file.

    In the terminal, type the following command and press Enter:

```
head -n1 /tmp/hello
```

Here, -n1 is an option that tells head to show only the first line. The 1 can be changed to any number to show that many lines.

You should see this output:
```
Hi,
```
This is just the first line of the file. By default, without the -n1 option, head would show the first 10 lines of the file.

--- 


# View the First Few Bytes of a File

Now we'll use the head command again, but this time to view a specific number of bytes from the beginning of a file.

In the terminal, type the following command and press Enter:
```
head -c1 /tmp/hello
```
The -c1 option tells head to show only the first byte (character) of the file. Like with -n, you can change the 1 to any number to see that many bytes.

You should see this output:
```
H
```
This is just the first character of the file. In text files, each character is typically one byte.

--- 

# Print the Last Lines of a File

Now let's move on to the tail command. As you might guess, tail is the opposite of head - it shows the end of a file.

In the terminal, type the following command and press Enter:
```
tail -n1 /tmp/hello
```
Just like with head, the -n1 option tells tail to show only one line, in this case the last line of the file.

You should see this output:
```
I am Labby!
```
This is the last line of our file. Without the -n1 option, tail would show the last 10 lines by default.

---


# View the Last Few Bytes of a File

Similar to what we did with head, we can use tail to display a specific number of bytes from the end of a file.

First, let's try viewing the last byte. In the terminal, type the following command and press Enter:
```
tail -c1 /tmp/hello
```
You might not see any output. This is because the last character is likely a newline character, which is invisible.

Let's try viewing the last two bytes instead. Type the following command and press Enter:

```
tail -c2 /tmp/hello
```
Now you should see:
```
!
```
The -c2 option tells tail to show the last 2 bytes (characters) of the file. In this case, it's showing the exclamation mark, which is the last visible character in our file.

--- 

# Comparing Files

Now we'll learn how to use the diff command to compare two files and see the differences between them.

First, let's make sure we're in the right directory (folder). Type the following command and press Enter:
```
cd ~/project
```
This changes our current directory to the "project" folder in our home directory. The ~ symbol is a shortcut for your home directory.

Now, let's compare two files. Type the following command and press Enter:
```
diff file1 file2
```
This tells diff to compare the contents of file1 and file2.

You should see output similar to this:
```
1c1
< this is file1
---
> this is file2
```

Let's break down what this output means. The diff command produces output that describes what changes are needed to make the first file identical to the second file. It doesn't matter which file was created or modified first; diff only compares their contents at the time you run the command.

 1c1: This indicates that line 1 in the first file needs to be changed to match line 1 in the second file.

< this is file1: The < symbol indicates a line from the first file (file1).

---: This is a separator between the lines from file1 and file2.
```>``` this is file2: The ```>``` symbol indicates a line from the second file (file2).

In simple terms, diff is showing us that the content of line 1 is different between the two files. To make file1 match file2, the line "this is file1" would need to be replaced with "this is file2".

# Comparing Directories

Finally, let's use the diff command to compare entire directories.

    In the terminal, type the following command and press Enter:
```
diff -r ~/Desktop ~/Code
```
The -r option tells diff to recursively compare subdirectories as well. ~/Desktop and ~/Code are the paths to the two directories we're comparing.

You might see output similar to this:
```
Only in /home/labex/Desktop: code.desktop
Only in /home/labex/Desktop: gedit.desktop
Only in /home/labex/Desktop: gvim.desktop
Only in /home/labex/Desktop: xfce4-terminal.desktop
```

This output shows that the Desktop directory contains four files that are not in the Code directory.

---

# Summary

Congratulations! You've completed the File Contents and Comparing lab. Let's recap what you've learned:

    You used cat to view the entire contents of a file.
    You learned how to use cat -n to view file contents with line numbers.
    You used head to view the beginning of a file, both by lines and by bytes.
    You used tail to view the end of a file, both by lines and by bytes.
    You learned how to use diff to compare the contents of files.
    Finally, you used diff -r to compare entire directories.

These commands are fundamental tools in Linux. As you continue to work with Linux, you'll find yourself using these commands frequently to inspect and compare files and directories.

Remember, if you ever forget how to use a command, you can always type man followed by the command name (e.g., man cat) to see the manual page for that command. This will give you detailed information about all the options available for each command.

Keep practicing with these commands on different files and directories to become more comfortable with them. The more you use them, the more natural they'll become!

--- 

# Creating a New File

Let's start by creating a new file using the touch command. This versatile command can create new, empty files and update the timestamps of existing ones. Think of it as a quick way to "touch" a file, either bringing it into existence or updating its last accessed time.

First, make sure you're in the right directory. We'll be working in your project directory:
```
cd ~/project
```
The cd command stands for "change directory." The ~ symbol represents your home directory, and /project specifies the subdirectory we want to move into. If the project directory doesn't exist, this command will likely fail. It's generally a good practice to create the directory first if you're unsure. However, in this lab environment, the directory should already exist.

Now, let's create a new file named example.txt:
```
touch example.txt
```
This command creates an empty file called example.txt in your current directory. To confirm that the file was created, use the ls command:
``` 
ls
```
ls stands for "list." It shows you the files and directories in your current location. You should see example.txt listed in the output. If you don't see it, double-check that you ran the touch command correctly and that you are indeed in the ~/project directory.

# Changing the Ownership of a File

Now that we've created a file, let's learn how to change its ownership. The chown command allows us to modify both the user and group ownership of a file. Ownership determines who has control over the file.

First, let's check the current ownership of our example.txt file:
```
ls -l example.txt
```
The ls -l command (list with long format) provides detailed information about the file, including its permissions, owner, and group. You should see output similar to this:
```
-rw-rw-r-- 1 labex labex 0 Jul 29 15:11 example.txt
```
Let's break down this output:

-rw-rw-r-- represents the file permissions (we'll explore this more in Step 4). The first character indicates the file type ( - for a regular file, d for directory, etc.). The remaining characters represent read, write, and execute permissions for the owner, group, and others.
The first labex is the current owner of the file. This is the username that owns the file.
The second labex is the current group of the file. A group is a collection of users that can share permissions.
0 is the file size in bytes. Since the file is empty, its size is zero.
Jul 29 15:11 is the last modified date and time.
example.txt is the file name.

Now, let's change the ownership of the file to the root user. root is the administrator account on Linux systems, and it has special privileges.
```
sudo chown root:root example.txt
```
Here's what this command does:

sudo runs the command with root privileges. You'll likely be prompted for your password. chown requires elevated privileges because it's a powerful command that can affect system security. Without sudo, you'll get a "Permission denied" error.
chown is the command to change ownership.
root:root specifies the new owner and group (both set to root). The syntax is owner:group.
example.txt is the target file.

Let's verify the change:
```
ls -l example.txt
```
You should now see that both the owner and group have changed to root:
```
-rw-rw-r-- 1 root root 0 Jul 29 15:11 example.txt
```
If you still see labex instead of root, make sure you used sudo when running the chown command and entered your password correctly

# Changing the Ownership of a Directory

The chown command can also change the ownership of entire directories and their contents. Let's see this in action. This is particularly useful for managing complex directory structures where you want to ensure all files and subdirectories have the same owner.

First, let's create a new directory with some files:
```
mkdir -p new-dir/subdir
echo "Hello, world" > new-dir/file1.txt
echo "Another file" > new-dir/subdir/file2.txt
```
Let's break down these commands:

mkdir -p new-dir/subdir creates the new-dir directory and its subdir subdirectory. The -p option tells mkdir to create parent directories as needed. Without -p, if new-dir didn't exist, creating new-dir/subdir would fail.
echo "Hello, world" > new-dir/file1.txt creates a file named file1.txt inside the new-dir directory and writes the text "Hello, world" into it. The > symbol is used for redirection; it takes the output of the echo command and redirects it into the specified file.
echo "Another file" > new-dir/subdir/file2.txt similarly creates a file named file2.txt inside the new-dir/subdir directory and writes the text "Another file" into it.

Now, let's check the current ownership:
```
ls -lR new-dir
```
ls -lR lists the contents of new-dir recursively. The -R option (recursive) makes ls list all files and subdirectories within new-dir and their contents.

You should see something like this:
```
new-dir:
total 4
-rw-rw-r-- 1 labex labex 13 Jul 29 09:15 file1.txt
drwxrwxr-x 2 labex labex 23 Jul 29 09:15 subdir

new-dir/subdir:
total 4
-rw-rw-r-- 1 labex labex 13 Jul 29 09:15 file2.txt
```
This shows that the directory new-dir, its subdirectory subdir, and the files file1.txt and file2.txt are all owned by labex.

Now, let's change the ownership of new-dir and all its contents to the root user:
```
sudo chown -R root:root new-dir
```
In this command:

The -R option tells chown to operate recursively, changing the ownership of all files and subdirectories within new-dir. This is crucial; without -R, only the new-dir directory's ownership would change, but the files and subdirectories within it would still be owned by labex.

Let's verify the change:
```
ls -lR new-dir
```
You should now see:
```
new-dir:
total 4
-rw-rw-r-- 1 root root 13 Jul 29 09:15 file1.txt
drwxrwxr-x 2 root root 23 Jul 29 09:15 subdir

new-dir/subdir:
total 4
-rw-rw-r-- 1 root root 13 Jul 29 09:15 file2.txt
```
As you can see, the ownership of the directory and all its contents has changed to root. This demonstrates the power of the -R option for making widespread changes to ownership within a directory structure.

# Changing the Permissions of a File

In Linux, file permissions are represented by a series of letters or numbers. Let's explore how to read and change these permissions. Understanding permissions is vital for securing your files and preventing unauthorized access.

First, let's look at the current permissions of our example.txt file:
```
ls -l example.txt
```
You might see something like this:
```
-rw-rw-r-- 1 root root 0 Jul 29 15:11 example.txt
```
The -rw-rw-r-- part represents the file permissions. This is where the numeric and symbolic notations come in. Let's break it down:

The first character (-) indicates this is a regular file. Other common indicators are d for directory and l for symbolic link.
The next three characters (rw-) represent the owner's permissions (read and write, but not execute).
        r stands for read permission: The owner can open and read the file.
        w stands for write permission: The owner can modify the file.
        x stands for execute permission: The owner can run the file (if it's a program or script). A - means the permission is denied.
    The next three (rw-) are for the group. They have the same meaning as above, but apply to members of the file's group.
    The last three (r--) are for others (everyone else). They also have the same meaning, but apply to users who are neither the owner nor members of the file's group.

Now, let's change these permissions using the chmod command. chmod stands for "change mode," and it allows you to modify these permissions. We'll start with the numeric notation.
```
sudo chmod 700 example.txt
```
In this command:

    700 is a numeric representation of permissions:
        The first digit (7) represents the owner's permissions.
        The second digit (0) represents the group's permissions.
        The third digit (0) represents the others' permissions.

Each digit is a number from 0 to 7, calculated by adding the values for read (4), write (2), and execute (1) permissions:

    4: Read permission
    2: Write permission
    1: Execute permission
    0: No permission

So, 7 (first digit) gives the owner

read (4), 

write (2), 

and execute (1) 

permissions: 4+2+1=7

0 (second digit) gives the group no permissions (0+0+0=0).

0 (third digit) gives others no permissions (0+0+0=0).

Therefore, 700 means: Owner: read, write, execute. Group: none. Others: none.

Let's verify the change:
```
ls -l example.txt
```
You should now see:
```
-rwx------ 1 root root 0 Jul 29 15:11 example.txt
```
The owner now has rwx (read, write, and execute) permissions, while the group and others have no permissions.

# Changing the Permissions of a Directory

Changing permissions for directories works similarly to changing permissions for files. Let's practice by creating a new directory and modifying its permissions. Directory permissions control who can list the directory's contents, create new files within the directory, and access files already in the directory.

First, let's create a new directory and set some non-standard permissions:
```
mkdir ~/test-dir
chmod 700 ~/test-dir
```
Now, let's check the current permissions:
```
ls -ld ~/test-dir
```
The -d option in ls -l tells ls to list the directory itself, rather than its contents. Without -d, ls would list the files and subdirectories inside test-dir, which is empty right now. You should see:

``` 
drwx------ 2 labex labex 4096 Jul 29 15:45 /home/labex/test-dir
```

The d at the beginning indicates that it's a directory. The rwx------ indicates that the owner has read, write, and execute permissions, while the group and others have no permissions. For directories:

- Read permission (r) allows you to list the contents of the directory using ls.
- Write permission (w) allows you to create new files and subdirectories within the directory.
- Execute permission (x) allows you to access files and subdirectories within the directory (i.e., cd into it).

Now, let's change the permissions:
```
chmod -R 755 ~/test-dir
```
In this command:

-R applies the change recursively to all files and subdirectories (though our directory is empty in this case). It's good practice to include it when dealing with directories, even if they're currently empty, in case you add files later.
755 gives read, write, and execute permissions to the owner, and read and execute permissions to group and others.

Let's break down 755:

    Owner (7): Read (4) + Write (2) + Execute (1) = 7

    Group (5): Read (4) + Execute (1) = 5

    Others (5): Read (4) + Execute (1) = 5

Let's verify the change:
```
ls -ld ~/test-dir
```
You should now see:
```
drwxr-xr-x 2 labex labex 4096 Jul 29 15:45 /home/labex/test-dir
```
This clearly shows the change in permissions, from only the owner having access (700) to the owner having full access while others can read and execute (755). Now, anyone can list the contents of test-dir and access files within it, but only the owner can create new files or modify existing ones.

# Using Symbolic Notation for Permissions

While numeric notation is concise, symbolic notation can be more intuitive, especially when you only want to change a single permission. Symbolic notation uses letters to represent the user, group, and others, and operators to add or remove permissions.

In this step, you'll create a small shell script and then add execute permission to it.

First, let's create a new script file with some content:
```
cd ~/project
echo '#!/bin/bash' > script.sh
echo 'echo "Hello, World"' >> script.sh
```
These commands do two things:

The first echo command creates script.sh and writes the first line, #!/bin/bash, into it. This line is called a shebang, and it tells Linux to run the script with Bash.
The second echo command adds a new line to the end of the file with >>. It writes echo "Hello, World", which will display Hello, World when the script runs.

You can confirm that the file now contains two separate lines with:
```
cat script.sh
```
You should see:
```
#!/bin/bash
echo "Hello, World"
```
Now, let's check its initial permissions:
```
ls -l script.sh
```
You should see something like:
```
-rw-rw-r-- 1 labex labex 32 Jul 29 16:30 script.sh
```
As you can see, initially, the script only has read and write permissions for the owner and group, and read permission for others. It doesn't have execute permission, which is required to run it as a program.

Let's try to run the script:
```
./script.sh
```
You should see a "Permission denied" error because the script doesn't have execute permissions yet. The ./ part tells the shell to execute the script located in the current directory.

Now, let's add execute permission for the owner using symbolic notation:
```
chmod u+x script.sh
```
In this command:

- u refers to the user (owner). Other options are g for group, o for others, and a for all (user, group, and others).

- +x adds execute permission. The + symbol adds a permission, while the - symbol removes a permission.

So, u+x means "add execute permission for the owner."

Let's verify the change:
```
ls -l script.sh
```
You should now see:
```
-rwxrw-r-- 1 labex labex 32 Jul 29 16:30 script.sh
```
The owner now has rwx (read, write, and execute) permissions.

Now, let's try running the script again:
```
./script.sh
```
This time, you should see the output:
```
Hello, World
```
This example clearly demonstrates why we need to add execute permissions to scripts, and the difference before and after adding these permissions. Symbolic notation makes it easy to modify specific permissions without having to recalculate the entire numeric representation.

## Summary

In this lab, we've explored essential Linux commands for managing file permissions:

We used touch to create new files and update existing ones.
We learned how to use chown to change file and directory ownership, including recursive changes for entire directory structures.
We practiced using chmod with both numeric and symbolic notation to modify file and directory permissions, understanding the different permission levels for owner, group, and others.
We saw practical examples of why permissions matter, such as needing execute permissions to run scripts.
We clarified the differences between numeric and symbolic notation for chmod and when each might be more appropriate.

These commands are crucial for maintaining security and controlling access in Linux systems. Remember to always be cautious when changing permissions, especially when using sudo, as incorrect changes can have significant consequences for system security and functionality. Always double-check your commands before executing them, and understand the implications of the changes you're making.

---


# Creating a New User

Let's start by creating a new user account named "joker".

Open a terminal. In Linux, the terminal is a text interface where you can enter commands.
Type the following command and press Enter:
```
sudo useradd joker
```
Let's break this down:

sudo is a command that gives you temporary superuser (administrator) privileges.We use it because creating a new user requires these higher-level permissions.
useradd is the command to create a new user.
joker is the username we're creating.

Note: If you try to run this command without sudo, you'll get a "permission denied" error. This is because regular users aren't allowed to create new user accounts - it's a task reserved for system administrators.

This highlights the difference between a superuser and a common user. As a common user, you can't create new user accounts, but by using sudo, you can temporarily elevate your privileges to perform this administrative task.

To verify that the user was created, we'll examine the /etc/passwd file:
```
sudo grep -w 'joker' /etc/passwd
```
The /etc/passwd file is like a phonebook for user accounts. Each line represents one user account, with different pieces of information separated by colons (:).

You should see output similar to:
```
joker:x:5001:5001::/home/joker:/bin/sh
```
This line shows:

-     Username: joker
-     Password: x (the actual password is stored securely elsewhere)
-     User ID: 5001
-     Group ID: 5001
-     Home Directory: /home/joker, but it hasn't been created yet
-     Default Shell: /bin/sh

# Creating a User with a Home Directory

Now, let's create another user named "bob" and give them a home directory.

Run the following command:
```
sudo useradd -m bob
```
The -m option tells the system to create a home directory for the user. A home directory is like a personal folder where a user can store their files and settings.

Let's verify that the home directory was created:
```
sudo ls -ld /home/bob
```
You should see output similar to:
```
drwxr-x--- 2 bob bob 57 Jan 19 13:33 /home/bob
```
This output shows:

d at the start means it's a directory
rwxr-x--- shows who can read, write, or execute in this directory
The two bob entries show that both the user and group owner of this directory is bob
57 is the size of the directory in bytes
Jan 19 13:33 is when the directory was created
/home/bob is the location of the directory

# Setting a User Password

Now we need to set a password for our new users. Let's set a password for "joker".

Run the following command:
```
sudo passwd joker
```
You'll be asked to enter a new password twice. For this lab, use a simple password like "password123".

- Important: The password will not be displayed as you type it. This is a security feature in Linux to prevent others from seeing your password as you type it. If you accidentally enter the wrong password, you can try again.
    Important: Remember this password! You'll need it later in the lab.

    If successful, you'll see a message saying "passwd: password updated successfully".

Note: In a real-world scenario, always use strong, unique passwords!

Behind the scenes, Linux stores encrypted passwords in a secure file called /etc/shadow. This is more secure than storing them in the /etc/passwd file where anyone could see them.


# Modifying User Properties

Linux allows us to change various settings for a user account after it's been created. Let's change joker's home directory as an example.

Run the following command:
```
sudo usermod -d /home/wayne joker
```
Here's what this does:

usermod is the command to modify user account settings
-d /home/wayne specifies the new home directory
joker is the user we're modifying

Let's verify the change:
```
sudo grep -w 'joker' /etc/passwd
```
- -w is used to match the whole word, and grep is used to search for the word in the file. You should see that joker's home directory has been updated in the output.


# Changing User Shell

Another important setting we can modify is the user's default shell. The shell is the program that interprets and runs the commands you type in the terminal.

By default, the user 'joker' is using /bin/sh as their shell. While sh (Bourne Shell) is a basic shell that's present on most Unix-like systems, bash (Bourne Again Shell) offers more features and is generally more user-friendly.

Changing joker's shell to bash provides several benefits:

    More intuitive command-line interface
    Enhanced scripting capabilities
    Better customization options for the user's environment

Here's how to make the change:

Change joker's default shell to bash:
```
sudo usermod -s /bin/bash joker
```
Verify the change:
```
sudo grep -w 'joker' /etc/passwd
```
You should see /bin/bash at the end of joker's entry. This means bash is now joker's default shell.

After making this change, joker will have access to the more feature-rich bash environment whenever they log in or open a new terminal session.

# Adding a User to a Group

In Linux, we use groups to organize users and manage permissions. One important group is the sudo group, which gives users administrative privileges. Let's add joker to the sudo group as an example.

Why would we add a user to the sudo group?

    System administration: Users in the sudo group can perform system-wide administrative tasks.
    Software installation: Sudo group members can install and update software packages.
    Configuration changes: They can modify system configuration files.
    User management: They can create, modify, or delete other user accounts.

You might wonder: "Why add someone to the sudo group when we can always use the 'sudo' command?" Here's why:

    Convenience: Users in the sudo group can use sudo without needing to know the root password. They use their own password instead.
    Granular control: System administrators can configure sudo to allow specific users to run only certain commands with superuser privileges.
    Accountability: Unlike sharing the root password, sudo logs who ran what command, improving security and traceability.
    Security: It's generally more secure to have named accounts with sudo access than to share the root password among multiple admins.

In a real-world scenario, you would typically add a user to the sudo group if:

    They are a system administrator or IT staff member who needs to perform regular maintenance tasks.
    They are a developer who needs to install specific software or make system changes for their work.
    They are a power user who needs elevated privileges for certain tasks, but you don't want to give them the root password.

Remember, adding a user to the sudo group gives them significant power over the system, so this should be done cautiously and only when necessary.

Now, let's add joker to the sudo group:

Run this command:
```
sudo usermod -aG sudo joker
```
Here's what this does:

usermod is the command to modify user accounts
-aG means "append to Group" (add to a group without removing from other groups)
sudo is the group we're adding the user to
joker is the user we're modifying

Verify the change:
```
groups joker
```
You should see sudo listed among joker's groups.

To see the effect of this change, we need to switch to the joker user and try a command that requires sudo privileges:
```
su - joker
```
This command switches from your current user (labex) to the joker user. You will be prompted to enter joker's password. Remember, this is the password you set earlier (password123). As you type the password, you won't see any characters on the screen - this is a security feature.

Once logged in as joker, let's try to view a file that normally requires root privileges:
```
sudo cat /etc/shadow
```
Enter joker's password again when prompted. You should be able to see the contents of the /etc/shadow file, which is usually only accessible to root. This confirms that joker now has sudo privileges.

After you're done, type exit to return to your original user account (labex).

- Note: In a production environment, you should be very careful about who you add to the sudo group. With great power comes great responsibility!


# Locking and Unlocking User Accounts

Sometimes, you might need to temporarily disable a user account without deleting it.

Lock the joker account:
```
sudo passwd -l joker
```
The -l option locks the password.

Try to switch to the joker user:
```
su - joker
```
You'll be asked for a password. Enter the password you set for joker earlier ("password123" if you followed our suggestion).

You should see an "authentication failure" message. This means the account is successfully locked.

Now, let's unlock the account:
```
sudo passwd -u joker
``` 
The -u option unlocks the password.

Try switching to the joker user again:
```
su - joker
```
Enter the password when prompted. This time, you should be able to switch to the joker user successfully.

Type exit to return to your original user account before continuing to the next step.

# Deleting a User

Finally, let's learn how to delete a user. We'll delete the "bob" user we created earlier.

Delete bob and their home directory:
```
sudo userdel -r bob
```
The userdel command deletes user accounts. The -r option removes the user's home directory and mail spool.

Verify that the user has been deleted:
```
sudo grep -w 'bob' /etc/passwd
sudo ls -ld /home/bob
```
Both commands should return no results. This means the user and their home directory have been successfully removed.


## Summary

Congratulations! You've completed the Linux User Account Management lab. You've learned how to:

    Create new user accounts
    Set user passwords
    Modify user properties like home directory and default shell
    Add users to groups
    Lock and unlock user accounts
    Delete user accounts

You've also been introduced to important Linux concepts like the /etc/passwd file, home directories, shells, and user groups. These are fundamental skills for Linux system administration. Remember, in real-world scenarios, always follow your organization's security policies when managing user accounts.


---

# First Login and Environment Check


Tasks

    Find out the username of the current user.
    Display the kernel name of the operating system.

Requirements

    All commands must be executed in the terminal.
    Use the whoami command to identify the current user.
    Use the uname command to show the kernel name.

Examples

After completing this step, you should see output similar to:
```
# Command output showing current user
labex

# Command output showing kernel name
Linux

```
---


# Checking System Information and Uptime


Tasks

    Display comprehensive system information including operating system details, kernel version, and hardware architecture.
    Check how long the system has been running and current system load.

Requirements

    Use the uname -a command to display all system information.
    Use the uptime command to show system uptime and load average.

--- 

# Gathering User and Group Details


Tasks

    Display the detailed user and group information for your current user account.

Requirements

    Use the id command to retrieve your user and group identifiers.


---

# Monitoring Real-time System Performance


Tasks

    Launch the interactive system monitoring tool to view active processes and resource usage.
    Exit the tool after observing the output for a few moments.

Requirements

    Use the top command to start the monitoring interface.
    After top is running, press the q key to exit and return to the command prompt.


---

# Generating a System Status Report


Tasks

    Create a file named system_report.txt in your current directory (~/project).
    The file must contain the output of the whoami, uname -a (all system information), and uptime commands.

Requirements

    The final report file must be named system_report.txt.
    You must use output redirection operators (> and >>) to write the command outputs into the file.
    The file must be created in the ~/project directory.

Examples

After completing this step, your system_report.txt file should contain output similar to:

labex
Linux labex-virtual-machine 5.15.0-76-generic #83-Ubuntu SMP Thu Jun 15 19:16:32 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
 10:50:01 up  1:20,  1 user,  load average: 0.00, 0.01, 0.05

This report file demonstrates:

    Line 1: Current user identity (from whoami command)
    Line 2: Complete system information including kernel version, hostname, and architecture (from uname -a command)
    Line 3: System uptime and current load averages (from uptime command)

The file serves as a snapshot of the system's current state, which is valuable for documentation and troubleshooting purposes. You can verify the file contents using the cat command after creation.
Hints

    Use the > operator to redirect the output of the first command. This will create the file (or overwrite it if it already exists).
    Use the >> operator to append the output of the subsequent commands to the file without deleting its existing content.
    The uptime command shows how long the system has been running.

--- 

# Setting Up the Project Directory Structure

Tasks

    Navigate into the ~/project/phoenix_project directory.
    Create three new subdirectories: src for source code, config for configuration files, and docs for documentation.

Requirements

    All new directories must be created inside the ~/project/phoenix_project directory.
    The directory names must be exactly src, config, and docs.
    You should use a single command to create all three directories simultaneously.

Examples

After completing this step, your directory structure should look like this:
```
~/project/phoenix_project/
├── config/
├── docs/
├── src/
├── README.md
├── config.json
└── main_app.py
```

When you run ls -F in the ~/project/phoenix_project directory, you should see:

README.md  config/  config.json  docs/  main_app.py  src/

The / symbols after directory names indicate they are directories, not files.
Hints

    Use the cd command to change your current directory.
    The mkdir command is used to create new directories.
    mkdir can accept multiple arguments to create several directories at once.

--- 


# Navigating and Creating Project Files


Tasks

    Move the main_app.py file into the src directory.
    Move the config.json file into the config directory.
    Move the README.md file into the docs directory.

Requirements

    Ensure you are in the ~/project/phoenix_project directory before performing the move operations.
    Use the mv command to relocate each file.

Examples

After moving the files, your project structure should be organized like this:
```
~/project/phoenix_project/
├── config/
│ └── config.json
├── docs/
│ └── README.md
└── src/
└── main_app.py
```

When you run ls -F in the root ~/project/phoenix_project directory, it should show only the directories:

config/  docs/  src/

Each file should now be in its appropriate subdirectory:

    ls src/ → main_app.py
    ls config/ → config.json
    ls docs/ → README.md

Hints

    The mv command is used to move or rename files and directories.
    The basic syntax is mv [SOURCE] [DESTINATION].
    For example, to move file.txt into a directory named documents, you would use mv file.txt documents/.

--- 

# Backing Up Critical Configuration Files

The config.json file contains critical settings for Project Phoenix. Before any modifications are made, it's a vital safety measure to create a backup. Your next task is to create a copy of this file.
Tasks

    Create a backup copy of the config.json file.

Requirements

    The backup file must be created within the ~/project/phoenix_project/config/ directory.
    The backup file must be named exactly config.json.bak.

Examples

After creating the backup, your config directory should contain both files:
```
~/project/phoenix_project/config/
├── config.json
└── config.json.bak
```


When you run ls in the ~/project/phoenix_project/config/ directory, you should see:

config.json  config.json.bak

Both files should have identical content, as the .bak file is an exact copy of the original:

# These commands should show identical output
cat config.json
cat config.json.bak

Hints

    The cp command is used to copy files and directories.
    The syntax is cp [SOURCE] [DESTINATION].
    You will need to provide the full path to the source file and the full path for the new backup file.


--- 


# Reorganizing the Team’s Shared Resources



    Move the entire shared_docs directory and all of its contents into the ~/project/phoenix_project/docs/ directory.

Requirements

    The source directory is ~/project/shared_docs.
    The destination path is ~/project/phoenix_project/docs/.
    The entire directory, not just its contents, must be moved.

Examples

After moving the shared_docs directory, your documentation structure should look like this:
```
~/project/phoenix_project/docs/
├── README.md
└── shared_docs/
├── api_spec.doc
└── team_guidelines.txt
```
When you run ls in the ~/project/phoenix_project/docs/ directory, you should see:

README.md  shared_docs/

The shared_docs directory should contain all its original files:

ls ~/project/phoenix_project/docs/shared_docs/

api_spec.doc  team_guidelines.txt

The original location ~/project/shared_docs should no longer exist.

Hints

    The mv command works for directories just as it does for files.
    When you move a directory, all of its contents are moved with it automatically.
    The command will look like mv [SOURCE_DIRECTORY] [DESTINATION_DIRECTORY].


---


# Archiving and Removing Outdated Log Files



The tar command is a powerful Linux tool for creating and manipulating archive files. "Tar" originally stood for "Tape Archive" because it was designed to write data to magnetic tapes, but today it's commonly used to create compressed archive files on disk.

When you use tar, you're essentially bundling multiple files together into a single file (called an archive), and you can optionally compress this archive to save space. The most common compression format is gzip, which adds the .gz extension to the filename.

The tar command uses different options (flags) to control its behavior:

    c: Create a new archive
    z: Compress the archive using gzip
    f: Specify the filename of the archive

So tar -czf archive.tar.gz file1 file2 creates a new compressed archive named archive.tar.gz containing file1 and file2.
Tasks

    Navigate to the ~/project/logs directory.
    Create a compressed tar archive named old_logs.tar.gz that contains all log files from the year 2023.
    After the archive is successfully created, delete the original 2023 log files that you just archived.

Requirements

    The final archive must be named exactly old_logs.tar.gz.
    The archive must be located in the ~/project/logs directory.
    Only log files with 2023 in their name should be archived and subsequently removed.
    The log file from 2024 (app_2024-05-01.log) must not be included in the archive and must not be deleted.

Examples

Before archiving, your logs directory contains:
```
~/project/logs/
├── app_2023-01-15.log
├── app_2024-05-01.log
└── db_2023-02-20.log
```
After completing the archiving task, your logs directory should look like:
```
~/project/logs/
├── app_2024-05-01.log
└── old_logs.tar.gz
```
When you run ls in the ~/project/logs/ directory, you should see:

app_2024-05-01.log  old_logs.tar.gz

Hints

    Use the tar command to create archives. The options -czf are a powerful combination: c (create), z (compress with gzip), and f (specify filename).
    You can use a wildcard (*) to select multiple files that match a pattern. For example, *_2023-*.log will match all files that end with .log and have _2023- in their name.
    The rm command is used to remove (delete) files. Be careful when using it with wildcards!


--- 


# Reviewing Application Log File Contents


Tasks

    Filter the ~/project/logs/app.log file to find all lines containing the word ERROR.
    Save the filtered lines to a new file named ~/project/error_report.txt.

Requirements

    You must use a command-line tool to search the file.
    The input file for your search is ~/project/logs/app.log.
    The output must be saved in a file named ~/project/error_report.txt in the ~/project directory.
    The output file should only contain the lines with the word ERROR.

Hints

    The grep command is perfect for searching for patterns in text files.
    To save the output of a command to a file, you can use the > redirection operator. This will create the file if it doesn't exist or overwrite it if it does.

Examples

After successfully filtering the log file, your ~/project/error_report.txt file should contain only the error lines:
```
$ cat ~/project/error_report.txt
[2023-10-26 10:00:03] ERROR: Failed to process payment transaction #12345.
[2023-10-26 10:00:05] ERROR: NullPointerException at com.innovatech.Billing.process(Billing.java:101).
```
The file should contain exactly 2 lines, both starting with timestamps and containing the word "ERROR".


---

# Investigating System Boot Messages


Tasks

    Examine the system's kernel messages for any lines related to fail or error.
    Save these findings into a file named ~/project/boot_issues.txt.

Requirements

    You must use the dmesg command to view kernel messages.
    Your search for fail or error should be case-insensitive.
    The results must be saved to a file named ~/project/boot_issues.txt.
    Note: You may need administrative privileges (sudo) to access kernel messages.

Hints

    The dmesg command displays kernel messages. You can "pipe" its output to another command for filtering.
    The pipe operator | sends the output of one command to the input of another.
    The grep command's -i option makes the search case-insensitive.
    To search for multiple patterns at once (like fail OR error), you can use grep -E 'pattern1|pattern2'.
    Note: If you encounter a "Operation not permitted" error, try running the command with sudo to gain the necessary privileges.

Examples

After successfully filtering the kernel messages, your ~/project/boot_issues.txt file should contain relevant system messages:
```
$ cat ~/project/boot_issues.txt
[    0.330755] acpi PNP0A03:00: fail to add MMCONFIG information, can't access extended PCI configuration space under this bridge.
[    1.026520] RAS: Correctable Errors collector initialized.
[   28.260800] kernel: [   10.123456] my-driver: probe of 0000:00:1f.0 failed with error -2
```
The file should contain kernel messages that include words like "fail" or "error" (case-insensitive), showing potential hardware or driver issues during system boot.

---

# Examining the Web Server Configuration File

Tasks

    Search the web server configuration file at ~/project/config/nginx.conf.
    Find the line containing the worker_processes directive.
    Append this line to the ~/project/error_report.txt file you created in the first step.

Requirements

    The input file is ~/project/config/nginx.conf.
    You must append the result to ~/project/error_report.txt, not overwrite it.

Hints

    You can use grep again for this task.
    To append output to a file instead of overwriting it, use the >> operator.

Examples

After appending the worker_processes line to your existing error report, the ~/project/error_report.txt file should now contain both the original error lines and the new configuration line:
```
$ cat ~/project/error_report.txt
[2023-10-26 10:00:03] ERROR: Failed to process payment transaction #12345.
[2023-10-26 10:00:05] ERROR: NullPointerException at com.innovatech.Billing.process(Billing.java:101).
worker_processes 4;
```
The file should contain 3 lines total: 2 original error lines plus 1 new line with "worker_processes 4;".

--- 


# Comparing Staging and Production Configuration Files

Tasks

    Compare the staging configuration file ~/project/config/staging/app.conf with the production configuration file ~/project/config/production/app.conf.
    Save the differences to a new file named ~/project/config_diff.txt.

Requirements

    You must use the diff command.
    The output showing the differences must be saved to ~/project/config_diff.txt.

Hints

    The diff command is designed specifically for comparing two files line by line.
    The basic syntax is diff file1 file2, where it shows what changes need to be made to file1 to make it identical to file2.
    The order of files matters! diff A B and diff B A will show different outputs.
    You can redirect the output of diff to a file just like you did with grep.

Examples

After comparing the staging and production configuration files, your ~/project/config_diff.txt file should show the differences between the two environments:
```
$ cat ~/project/config_diff.txt
1,5c1,5
< # Staging Configuration
< database.url=jdbc:mysql://staging-db:3306/nexus
< api.key=staging_key_abc123
< feature.flag.new_dashboard=true
< timeout.ms=3000
---
> # Production Configuration
> database.url=jdbc:mysql://prod-db:3306/nexus
> api.key=prod_key_xyz789
> feature.flag.new_dashboard=false
> timeout.ms=5000
```
The diff output shows what changes would need to be made to the staging configuration file to make it match the production configuration file. Lines starting with < show content from the staging file, while lines starting with > show content from the production file. This reveals that the production environment uses different database URLs, API keys, feature flags, and timeout values compared to staging.


--- 

# Verifying Directory Consistency Between Servers

Tasks

    You have two directories: /home/labex/project/server1_files (representing the staging server) and /home/labex/project/server2_files (representing the production server).
    Compare these two directories to find out which files are unique to server1_files.
    Save the complete comparison output to a file named /home/labex/project/missing_files.txt.

Requirements

    You must use the diff command to compare the two directories.
    The output must be saved to /home/labex/project/missing_files.txt.

Hints

    The diff command can also compare directories if you provide directory paths instead of file paths.
    Using the -r or --recursive option with diff is a good practice for comparing directories, as it will compare all files within them.
    The output format of diff on directories will explicitly state which files are "Only in" a specific directory.
    Just like with files, the order matters when comparing directories. diff dir1 dir2 shows what's in dir1 but not in dir2, while diff dir2 dir1 shows the opposite.

Examples

After comparing the two server directories, your /home/labex/project/missing_files.txt file should show which files are missing from the production server:
```
$ cat /home/labex/project/missing_files.txt
Only in /home/labex/project/server1_files: asset2.js
```
This output indicates that asset2.js exists in the first directory (server1_files, representing the staging server) but is missing from the second directory (server2_files, representing the production server). By comparing staging first and production second, we can easily identify files that are missing from production, which could explain some of the application failures.

--- 


# Creating a Secure File for a New Project


Tasks

    Create a new, empty file named project_keys.txt inside the ~/project/phoenix_project directory.
    Set the permissions for this file so that only the owner has read and write access, and no one else (not even users in the same group) has any access.

Requirements

    The file must be named project_keys.txt.
    The file must be located at ~/project/phoenix_project/project_keys.txt.
    Use the chmod command with numeric notation to set the permissions.

Hints

    You can create an empty file using the touch command.
    Remember the numeric values for permissions: read (4), write (2), and execute (1).
    The final permission should be 600 (read+write for owner, nothing for group and others).

Examples

After completing this task, you should see something like:
```
$ ls -l ~/project/phoenix_project/
-rw------- 1 labex labex 0 Sep 3 16:03 project_keys.txt
```
The file permissions show -rw-------, indicating:

    Owner has read and write permissions
    Group has no permissions
    Others have no permissions


---

# Assigning Ownership of Project Resources


Tasks

    Change the owner of the ~/project/phoenix_project directory and all its contents to the user dev_lead.
    Change the group owner of the ~/project/phoenix_project directory and all its contents to the developers group.

Requirements

    The user owner must be dev_lead.
    The group owner must be developers.
    The ownership change must apply recursively to all files and subdirectories within ~/project/phoenix_project.
    You must use the chown command.

Hints

    The chown command can change both user and group at the same time using the user:group syntax.
    Look for an option in the chown command that allows it to operate on files and directories recursively. The man chown command is your friend.
    Since the files are currently owned by root, you will need to use sudo to change ownership.

Examples

After completing this task, you should see something like:
```
$ ls -ld ~/project/phoenix_project/
drwxrwxr-x 4 dev_lead developers 53 Sep 3 16:00 ~/project/phoenix_project/

$ ls -l ~/project/phoenix_project/
total 0
drwxrwxr-x 2 dev_lead developers 27 Sep 3 16:00 docs
-rw------- 1 dev_lead developers 0 Sep 3 16:03 project_keys.txt
drwxrwxr-x 2 dev_lead developers 6 Sep 3 16:00 src
```
All files and directories should now be owned by:

    User: dev_lead
    Group: developers


---

# Securing the Main Project Directory


Tasks

    Set the permissions for the ~/project/phoenix_project directory.

Requirements

    The owner (dev_lead) must have read, write, and execute permissions.
    The group (developers) must have read and execute permissions.
    Others must have no permissions.
    Use the chmod command to apply these permissions to the ~/project/phoenix_project directory itself (not recursively).
    Since the directory is owned by dev_lead, you may need to use sudo to change permissions.

Hints

    "Execute" permission on a directory allows you to cd into it.
    Calculate the numeric permission value for owner, group, and others.
    Owner (rwx) = 4+2+1 = 7
    Group (r-x) = 4+0+1 = 5
    Others (---) = 0+0+0 = 0

Examples

After completing this task, you should see something like:
```
$ ls -ld ~/project/phoenix_project/
drwxr-x--- 4 dev_lead developers 53 Sep 3 16:00 ~/project/phoenix_project/
```
The directory permissions show drwxr-x---, indicating:

    Owner (dev_lead) has read, write, and execute permissions
    Group (developers) has read and execute permissions
    Others have no permissions

This means:

    dev_lead can fully access the directory
    developers group members can list contents and enter the directory
    Outsiders have no access to the directory

--- 


# Setting Up Collaborative Permissions for the Dev Team

    Note: Make sure you have completed Step 2 first, which sets the ownership of all project directories (including src) to dev_lead:developers. This step builds upon those ownership settings.


Tasks

    Set a special permission on the ~/project/phoenix_project/src directory that forces all new files and subdirectories created within it to inherit the group ownership from the src directory itself (which is developers).

Requirements

    The solution must ensure new files in ~/project/phoenix_project/src automatically inherit the developers group.
    You must use the chmod command to set this special permission.
    You may need to use sudo to set permissions on directories owned by other users.

Hints

    This special permission is called the "set group ID" or setgid bit.
    You can apply the setgid bit using either symbolic (g+s) or numeric notation.
    In numeric notation, the setgid bit has a value of 2. It is placed before the standard three permission digits (e.g., 2770).

Examples

After completing this task, you should see something like:
```
$ ls -ld ~/project/phoenix_project/src/
drwxrws--- 2 dev_lead developers 6 Sep 3 16:00 ~/project/phoenix_project/src/
```
The s in the group execute position indicates the setgid bit is set and the group has execute permission. Now when you create a new file:

```
$ touch ~/project/phoenix_project/src/new_file.txt
$ ls -l ~/project/phoenix_project/src/new_file.txt
-rw-rw-r-- 1 labex developers 0 Apr 15 18:28 /home/labex/project/phoenix_project/src/new_file.txt
```
Notice that the new file automatically belongs to the developers group, even if you are logged in as a different user. The file owner still remains the user who created the file, while the group owner is inherited from the src directory. This ensures collaborative work within the development team while maintaining proper group ownership.

The permissions show:

Owner (dev_lead) has read and write permissions

Group (developers) has read and write permissions

Others have no permissions
The lowercase s in the group execute position indicates the setgid bit is set and the group has execute permission


---


# Onboarding a New Developer to the System


Tasks

    Create a new user account for Brenda Smith.

Requirements

    The username must be b.smith.
    Use the useradd command to add the new user to the system. You will need sudo privileges.

Hints

    This challenge expects the standard useradd command rather than the interactive adduser helper.
    Remember to use sudo to execute commands with administrative privileges.

Examples

After successfully creating the new user account, you should see the user entry in the system's user database:

$ grep "b.smith" /etc/passwd
b.smith:x:5002:5004::/home/b.smith:/bin/sh

The user account will be created with a system-assigned user ID and group ID. You can verify the account exists and check its details using:

$ id b.smith
uid=5002(b.smith) gid=5004(b.smith) groups=5004(b.smith)

--- 

# Creating a Dedicated Home Directory for the New User

You've created the user, but you forgot a crucial step! Brenda, as the senior developer leading Project Phoenix's final phase, needs her own secure workspace to store critical project files and development tools. You must ensure that a home directory is created for her.
Tasks

    Create a home directory for the user b.smith located at /home/b.smith.

Requirements

    The home directory must be created for the user b.smith.
    You should use an option with the useradd command to create the home directory automatically. If you have already created the user without a home directory, you may need to delete the user first and then recreate it correctly.
    Valid solutions include either -m or --create-home, and the flag may appear before or after the username.

Hints

    To delete a user, you can use the userdel command. For example: sudo userdel b.smith.
    The useradd command has a specific flag to create a home directory for the user. Check the man useradd page for an option like -m or --create-home.

Examples

After creating the user with a home directory, you should see the new directory created in the home directory listing:
```
$ ls -la /home/
drwxr-xr-x 1 root root 47 Sep 3 16:32 .
drwxr-xr-x 1 root root 62 Sep 3 16:31 ..
-rw-r--r-- 1 root root 58 Jul 18 2024 .zshrc
drwxr-x--- 2 b.smith b.smith 57 Sep 3 16:32 b.smith
drwxr-x--- 2 j.doe j.doe 57 Sep 3 16:31 j.doe
drwxr-x--- 1 labex labex 4096 Sep 3 16:35 labex
```
The home directory will be owned by the user with restricted permissions (accessible only by the owner and group). To view the contents, you may need appropriate permissions or use sudo:
```
$ sudo ls -la /home/b.smith/
drwxr-x--- 2 b.smith b.smith 57 Sep 3 16:32 .
drwxr-xr-x 1 root root 47 Sep 3 16:32 ..
-rw-r--r-- 1 b.smith b.smith 220 Sep 3 16:32 .bash_logout
-rw-r--r-- 1 b.smith b.smith 3771 Sep 3 16:32 .bashrc
-rw-r--r-- 1 b.smith b.smith 655 Sep 3 16:32 .profile
```
---


# Assigning an Initial Password for the New User


Tasks

    Set a password for the user b.smith.

Requirements

    Use the standard Linux command to change a user's password.
    You will be prompted to enter and confirm the new password. You can use any simple password, for example, password123.

Hints

    The command to set or change passwords is passwd.
    Since you are changing the password for another user, you will need sudo privileges. The syntax is sudo passwd <username>.

Examples

After setting the password successfully, the user account should have a password hash in the shadow file. You can verify this by checking the shadow file (note: this requires root privileges):
```
$ sudo grep "^b.smith:" /etc/shadow
b.smith:$y$j9T$XbJLH9LJgY518Th4qcd1V0$NrfHOJ2MGm/1OhLGfpfMQkvPasV23Eenhwl9bA0i8O4:20334:0:99999:7:::
```
--- 

# Adding the New Developer to the "developers" Group

Tasks

    Add the user b.smith to the developers group.

Requirements

    The user b.smith must be a member of the developers group.
    The user's existing group memberships should not be removed.

Hints

    The usermod command is used to modify a user account.
    Look for the -a (append) and -G (groups) flags. Using them together ensures you add the user to a new group without removing them from existing ones.

Examples

After successfully adding the user to the developers group, you should see the group membership reflected in the user's group list:
```
$ groups b.smith
b.smith : b.smith developers
```
You can also verify using the id command to see more detailed group information:
```
$ id b.smith
uid=5002(b.smith) gid=5004(b.smith) groups=5004(b.smith),5003(developers)
```
The user should now have access to files and directories that are accessible to the developers group. You can check the group file to confirm the group exists:
```
$ grep "^developers:" /etc/group
developers:x:5003:b.smith
```
Notice that b.smith appears in the list of group members. This confirms the user has been successfully added to the group while preserving their existing group memberships.


--- 


# Temporarily Disabling a Departing Employee’s Account


Tasks

    Lock the user account for j.doe to prevent logins.

Requirements

    The user account j.doe must be locked.
    Do not delete the user or their home directory.

Hints

    You can use the usermod command with the -L (lock) option.
    Alternatively, the passwd command has a -l (lock) flag that achieves the same result.
    Remember to use sudo.

Examples

You can verify the account is locked by checking the shadow file:
```
$ sudo grep "^j.doe:" /etc/shadow
j.doe:!:20334:0:99999:7:::
```
Notice the exclamation mark (!) at the beginning of the password field - this indicates the account is locked. The original password hash is preserved after the ! for potential future unlocking.

--- 

