 # Copying Files

The dd command is a utility for copying files or entire partitions at the bit level.

dd [OPTIONS] OPERAND

This command has several useful features, including:

    It can be used to clone or delete (wipe) entire disks or partitions.
    It can be used to copy raw data to removable devices, such as USB drives and CDROMs.
    It can backup and restore the MBR (Master Boot Record).
    It can be used to create a file of a specific size that is filled with binary zeros, which can then be used as a swap file (virtual memory).

Let's examine the following example. The dd command creates a file named /tmp/swapex with 50 blocks of zeros that are one megabyte in size:

Follow Along

Use the following cd command to return to the home directory:

sysadmin@localhost:~/Documents$ cd ~

sysadmin@localhost:~$ dd if=/dev/zero of=/tmp/swapex bs=1M count=50 
50+0 records in
50+0 records out
52428800 bytes (52 MB) copied, 0.825745 s, 635 MB/s

The dd command uses special arguments to specify how it will work. The following illustrates some of the more commonly used arguments:
Argument 	Description
if 	

Input File: The input file to be read from.

dd if=/dev/zero of=/tmp/swapex bs=1M count=50 

The example reads from the /dev/zerofile, a special file containing an unlimited number of zeros.
of 	

Output File: The output file to be written.

dd if=/dev/zero of=/tmp/swapex bs=1M count=50

bs 	

Block Size: The block size to be used. By default, the value is considered to be in bytes. Use the following suffixes to specify other units: K, M, G, and T for kilobytes, megabytes, gigabytes and terabytes respectively.

dd if=/dev/zero of=/tmp/swapex bs=1M count=50

The example uses a block size of one megabyte.
count 	

Count: The number of blocks to be read from the input file.

dd if=/dev/zero of=/tmp/swapex bs=1M count=50

The example command reads 50 blocks.

Consider This

No block size or count needs to be specified when copying over entire devices. For example, to clone from one hard drive (/dev/sda) to another (/dev/sdb) execute the following command:

dd if=/dev/sda of=/dev/sdb

---

#  Filtering Input

The grep command is a text filter that will search input and return lines which contain a match to a given pattern.

grep [OPTIONS] PATTERN [FILE]

Follow Along

Use the following command to switch to the Documents directory:

sysadmin@localhost:~$ cd ~/Documents

If the example below fails, repeat the example from Section 11: Copying Files:

sysadmin@localhost:~/Documents$ cp /etc/passwd .

For example, the passwd file we previously copied into the Documents directory contains the details of special system accounts and user accounts on the system. This file can be very large, however the grep command can be used to filter out information about a specific user, such as the sysadmin user. Use sysadmin as the pattern argument and passwd as the file argument:

sysadmin@localhost:~/Documents$ grep sysadmin passwd                               
sysadmin:x:1001:1001:System Administrator,,,,:/home/sysadmin:/bin/bash 

The command above returned the line from the passwd which contains the pattern sysadmin.

Note

This line is the /etc/passwd entry pertaining to the user sysadmin and provides information that is beyond the scope of this course. To learn more about this file, check out NDG Linux Essentials.

The example above uses a simple search term as the pattern, however grep is able to interpret much more complex search patterns.

---

#  Regular Expressions

Regular expressions have two common forms: basic and extended. Most commands that use regular expressions can interpret basic regular expressions. However, extended regular expressions are not available for all commands and a command option is typically required for them to work correctly.

The following table summarizes basic regular expression characters:
Basic Regex Character(s) 	Meaning
. 	Any one single character
[ ] 	Any one specified character
[^ ] 	Not the one specified character
* 	Zero or more of the previous character
^ 	If first character in the pattern, then pattern must be at beginning of the line to match, otherwise just a literal ^
$ 	If last character in the pattern, then pattern must be at the end of the line to match, otherwise just a literal $

The following table summarizes the extended regular expressions, which must be used with either the egrep command or the -E option with the grep command:
Extended Regex Character(s) 	Meaning
+ 	One or more of the previous pattern
```
? 	The preceding pattern is optional.

{ } 	Specify minimum, maximum or exact matches of the previous pattern.

| 	Alternation - a logical "or".

( ) 	Used to create groups.

```



---

#  Basic Patterns

Regular expressions are patterns that only certain commands are able to interpret. Regular expressions can be expanded to match certain sequences of characters in text. The examples displayed on this page will make use of regular expressions to demonstrate their power when used with the grep command. In addition, these examples provide a very visual demonstration of how regular expressions work, the text that matches will be displayed in a red color.

Follow Along

Use the following cd command to change to the Documents directory.
```
sysadmin@localhost:~$ cd ~/Documents                                                 
```

The simplest of all regular expressions use only literal characters, like the example from the previous page:
```
sysadmin@localhost:~/Documents$ grep sysadmin passwd                             
```
```
sysadmin:x:1001:1001:System Administrator,,,,:/home/sysadmin:/bin/bash
```
### Anchor Characters

Anchor characters are one of the ways regular expressions can be used to narrow down search results. For example, the pattern root appears many times in the /etc/passwd file:
```
sysadmin@localhost:~/Documents$ grep 'root' passwd
root:x:0:0:root:/root:/bin/bash                                                 
operator:x:1000:37::/root:
```

To prevent the shell from misinterpreting them as special shell characters, these patterns should be protected by strong quotes, which simply means placing them between single quotes.

The first anchor character ^ is used to ensure that a pattern appears at the beginning of the line. For example, to find all lines in /etc/passwd that start with root use the pattern ^root. Note that ^ must be the first character in the pattern to be effective.
```
sysadmin@localhost:~/Documents$ grep '^root' /etc/passwd
root:x:0:0:root:/root:/bin/bash
```

For the next example, first examine the alpha-first.txt file. The cat command can be used to print the contents of a file:
```
sysadmin@localhost:~/Documents$ cat alpha-first.txt                             
A is for Animal                                                                 
B is for Bear                                                                   
C is for Cat                                                                    
D is for Dog                                                                    
E is for Elephant                                                               
F is for Flower
```
The second anchor character $ can be used to ensure a pattern appears at the end of the line, thereby effectively reducing the search results. To find the lines that end with an r in the alpha-first.txt file, use the pattern r$:
```
sysadmin@localhost:~/Documents$ grep 'r$' alpha-first.txt
B is for Bear
F is for Flower
```

Again, the position of this character is important, the $ must be the last character in the pattern in order to be effective as an anchor.

### Match a Single Character With .

The following examples will use the red.txt file:
```
sysadmin@localhost:~/Documents$ cat red.txt
red
reef
rot
reeed
rd
rod
roof
reed
root
reel
read
```
One of the most useful expressions is the period . character. It will match any character except for the new line character. The pattern r..f would find any line that contained the letter r followed by exactly two characters (which can be any character except a newline) and then the letter f:
``` 
sysadmin@localhost:~/Documents$ grep 'r..f' red.txt
reef
roof
```

The same concept can be repeated using other combinations. The following will find four letter words that start with r and with d:
```
sysadmin@localhost:~/Documents$ grep 'r..d' red.txt
reed
read
```
This character can be used any number of times. To find all words that have at least four characters the following pattern can be used:
```
sysadmin@localhost:~/Documents$ grep '....' red.txt                             
reef
reeed
roof                                                                            
reed
root
reel
read
```
The line does not have to be an exact match, it simply must contain the pattern, as seen here when r..t is searched for in the /etc/passwd file:
```
sysadmin@localhost:~/Documents$ grep 'r..t' /etc/passwd
root:x:0:0:root:/root:/bin/bash
operator:x:1000:37::/root:  
``` 

### Match a Single Character With []

The square brackets [ ] match a single character from the list or range of possible characters contained within the brackets.

For example, given the profile.txt file:
```
sysadmin@localhost:~/Documents$ cat profile.txt
Hello my name is Joe.
I am 37 years old.
3121991
My favorite food is avocados.
I have 2 dogs.
123456789101112
```

To find all the lines in the profile.txt which have a number in them, use the pattern [0123456789] or [0-9]:
```
sysadmin@localhost:~/Documents$ grep '[0-9]' profile.txt
I am 37 years old.
3121991
I have 2 dogs.
123456789101112
```

On the other hand, to find all the lines which contain any non-numeric characters, insert a ^ as the first character inside the brackets. This character negates the characters listed:
```
sysadmin@localhost:~/Documents$ grep '[^0-9]' profile.txt
Hello my name is Joe.
I am 37 years old.
My favorite food is avocados.
I have 2 dogs.
```

Note

Do not mistake [^0-9] to match lines which do not contain numbers. It actually matches lines which contain non-numbers. Look at the original file to see the difference. The third and sixth lines only contain numbers, they do not contain non-numbers so those lines do not match.

When other regular expression characters are placed inside of square brackets, they are treated as literal characters. For example, the . normally matches any one character, but placed inside the square brackets, then it will just match itself. In the next example, only lines which contain the . character are matched.
```
sysadmin@localhost:~/Documents$ grep '[.]' profile.txt
Hello my name is Joe.
I am 37 years old.
My favorite food is avocados.
I have 2 dogs.
```

### Match a Repeated Character Or Patterns With *

The regular expression character * is used to match zero or more occurrences of a character or pattern preceding it. For example e* would match zero or more occurrences of the letter e:
```
sysadmin@localhost:~/Documents$ cat red.txt
red
reef
rot
reeed
rd
rod
roof
reed
root
reel
read
sysadmin@localhost:~/Documents$ grep 're*d' red.txt
red
reeed
rd
reed
```

It is also possible to match zero or more occurrences of a list of characters by utilizing the square brackets. The pattern [oe]* used in the following example will match zero or more occurrences of the o character or the e character:
```
sysadmin@localhost:~/Documents$ grep 'r[oe]*d' red.txt
red
reeed
rd
rod
reed
```

When used with only one other character, * isn't very helpful. Any of the following patterns would match every string or line in the file: .* e* b* z*.
```
sysadmin@localhost:~/Documents$ grep 'z*' red.txt
red
reef
rot
reeed
rd
rod
roof
reed
root
reel
read
```
```
sysadmin@localhost:~/Documents$ grep 'e*' red.txt
red
reef
rot
reeed
rd
rod
roof
reed
root
reel
read
```

This is because * can match zero occurrences of a pattern. In order to make the * useful, it is necessary to create a pattern which includes more than just the one character preceding *. For example, the results above can be refined by adding another e to make the pattern ee* effectively matching every line which contains at least one e.
```
sysadmin@localhost:~/Documents$ grep 'ee*' red.txt
red
reef
reeed
reed
reel
read
```

### Standard Input

If a file name is not given, the grep command will read from standard input, which normally comes from the keyboard with input provided by the user who runs the command. This provides an interactive experience with grep where the user types in the input and grep filters as it goes. Feel free to try it out, just press Ctrl-D when you're ready to return to the prompt.

Follow Along

Use the following cd command to return to the home directory:
```
sysadmin@localhost:~/Documents$ cd ~
```

--- 

---

---

# Linux Fundamentals

Before you can master Kali Linux, you must be at ease with a generic Linux system. Linux proficiency will serve you well, because a large percentage of web, email, and other Internet services run on Linux servers.

In this section, we strive to cover the basics of Linux, but we assume that you already know about computer systems in general, including components such as the CPU, RAM, motherboard, and hard disk, as well as device controllers and their associated connectors.

###  What Is Linux and What Is It Doing?

The term "Linux" is often used to refer to the entire operating system, but in reality, Linux is the operating system kernel, which is started by the boot loader, which is itself started by the BIOS/UEFI. The kernel assumes a role similar to that of a conductor in an orchestra—it ensures coordination between hardware and software. This role includes managing hardware, processes, users, permissions, and the file system. The kernel provides a common base to all other programs on the system and typically runs in ring zero, also known as kernel space.

- Let's quickly review the various tasks handled by the Linux kernel.

#### Driving Hardware

The kernel exports data about detected hardware through the /proc/ and /sys/ virtual file systems. Applications often access devices by way of files created within /dev/. Specific files represent disk drives (for instance, /dev/sda), partitions (/dev/sda1), mice (/dev/input/mouse0), keyboards (/dev/input/event0), sound cards (/dev/snd/*), serial ports (/dev/ttyS*), and other components.

There are two types of device files: block and character. The former has characteristics of a block of data: It has a finite size, and you can access bytes at any position in the block. The latter behaves like a flow of characters. You can read and write characters, but you cannot seek to a given position and change arbitrary bytes. To find out the type of a given device file, inspect the first letter in the output of ls -l. It is either b, for block devices, or c, for character devices:

```
$ ls -l /dev/sda /dev/ttyS0
brw-rw---- 1 root disk    8,  0 Mar 21 08:44 /dev/sda
crw-rw---- 1 root dialout 4, 64 Mar 30 08:59 /dev/ttyS0
```
As you might expect, disk drives and partitions use block devices, whereas mouse, keyboard, and serial ports use character devices. In both cases, the programming interface includes device-specific commands that can be invoked through the ioctl system call.

## Unifying File Systems

- The starting point of this hierarchical tree is called the root, represented by the "/" character. This directory can contain named subdirectories. For instance, the home subdirectory of / is called /home/. This subdirectory can, in turn, contain other subdirectories, and so on. Each directory can also contain files, where the data will be stored. Thus, /home/kali/Desktop/hello.txt refers to a file named hello.txt stored in the Desktop subdirectory of the kali subdirectory of the home directory, present in the root. The kernel translates between this naming system and the storage location on a disk.

- 
There are many file system formats, corresponding to many ways of physically storing data on disks. The most widely known are ext2, ext3, and ext4, but others exist. For instance, VFAT is the filesystem that was historically used by DOS and Microsoft Windows operating systems. Linux's support for VFAT allows hard disks to be accessible under Kali as well as under Microsoft Windows. In any case, you must prepare a file system on a disk before you can mount it and this operation is known as formatting. Commands such as mkfs.ext4 (where mkfs stands for MaKe FileSystem) handle formatting. These commands require, as a parameter, a device file representing the partition to be formatted (for instance, /dev/sda1, the first partition on the first drive). This operation is destructive and should be run only once, unless you want to wipe a filesystem and start fresh.

## Managing Processes

A process is a running instance of a program, which requires memory to store both the program itself and its operating data. The kernel is in charge of creating and tracking processes. When a program runs, the kernel first sets aside some memory, loads the executable code from the file system into it, and then starts the code running. It keeps information about this process, the most visible of which is an identification number known as the process identifier (PID).

## Multi-Processor Systems (and Variants)

The limitation described above, of only one process running at a time, doesn't always apply: the actual restriction is that there can be only one running process per processor core. Multi-processor, multi-core, or hyper-threaded systems allow several processes to run in parallel. The same time-slicing system is used, though, to handle cases where there are more active processes than available processor cores. This is not unusual: a basic system, even a mostly idle one, almost always has tens of running processes.

## Rights Management

Unix-like systems support multiple users and groups and allow control of permissions. Most of the time, a process is identified by the user who started it. That process is only permitted to take actions permitted for its owner.

## The Command Line

By "command line", we mean a text-based interface that allows you to enter commands, execute them, and view the results. You can run a terminal (a textual screen within the graphical desktop, or the text console itself outside of any graphical interface) and a command interpreter inside it (the shell).

The program handling your input and executing your commands is called a shell (or a command-line interpreter). The default shell provided in Kali Linux is ZSH (it stands for Z SHell). The trailing "$" or "#" character indicates that the shell is awaiting your input. It also indicates whether ZSH recognizes you as a normal user (the former case with the dollar, $) or as a super user (the latter case with the hash, #).

Once a session is open, the pwd command (which stands for print working directory) displays your current location in the filesystem. The current directory is changed with the cd directory command (cd is for change directory). When you don't specify the target directory, you are taken to your home directory. When you use cd - (dash), you go back to the former working directory (the one in use before the last cd call). The parent directory is always called .. (two dots), whereas the current directory is also known as . (one dot). The ls command allows listing the contents of a directory. If you don't provide parameters, ls operates on the current directory.

```bash
$ pwd
/home/kali
$ cd Desktop
$ pwd
/home/kali/Desktop
$ cd .
$ pwd
/home/kali/Desktop
$ cd ..
$ pwd
/home/kali
$ ls
Desktop    Downloads  Pictures  Templates
Documents  Music      Public    Videos
```

You can create a new directory with ```mkdir directory```, and remove an existing (empty) directory with ```rmdir directory```. The ```mv``` command allows moving and renaming files and directories; removing a file is achieved with ```rm file```, and copying a file is done with ```cp source-file target-file```.


The shell executes commands by searching for the corresponding executable within directories specified in the PATH environment variable—typically /bin, /sbin, /usr/bin, and /usr/sbin. While the which utility identifies the location of these external binaries, some commands (e.g., cd, pwd) are shell built-ins executed directly by the shell itself. The type command can be used to distinguish between these categories.

* ```PATH Hijacking```: If an attacker gains write access to a directory listed early in the PATH (or modifies the variable itself), they can place a malicious executable with the same name as a common command (e.g., ls). This allows for privilege escalation or credential harvesting when an unsuspecting user executes the "spoofed" command.

* ```Binary Proxying```: Understanding whether a command is a built-in or an external binary is vital for forensic analysis and EDR (Endpoint Detection and Response) monitoring. External binaries create new processes that leave distinct audit trails, whereas built-ins may execute within the context of the current shell process.

Environment Manipulation: Secure scripts should ideally use absolute paths (e.g., /bin/ls instead of ls) to negate the risk of path-based attacks and ensure the integrity of the executed software.

```bash
$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
$ which ls
/bin/ls
$ type rm
rm is /bin/rm
$ type cd
cd is a shell builtin
```

## Environment Variables & Inheritance

Environment variables serve as a global storage mechanism for configuration settings used by the shell and various applications. These variables are contextual, meaning each process maintains its own unique set, yet they are inheritable, allowing a parent process (like a login shell) to pass its variables down to any child programmes it executes.

System-wide configurations are typically defined in /etc/profile, while user-specific settings reside in ~/.profile. However, for variables intended to persist across all user sessions regardless of whether a shell is invoked, /etc/environment is the preferred location. This is facilitated by the Pluggable Authentication Module (PAM), which injects these variables during the session initiation phase.


Privilege Escalation via Inheritance: When a process spawns a child with higher privileges (e.g., via sudo or a SUID binary), insecure inheritance of variables like LD_PRELOAD or PYTHONPATH can allow an attacker to inject malicious libraries and execute arbitrary code with elevated permissions.

* Persistence Mechanisms: Attackers often target files like ~/.profile or /etc/environment to establish persistence. By injecting malicious commands or modifying the PATH within these files, they ensure their code executes automatically every time a user logs in or a new session is created.

* Information Leakage: Environment variables frequently store sensitive data such as API keys, database credentials, or session tokens. If a system is compromised or if process memory is dumped, these "global" settings can provide an attacker with the "keys to the kingdom" across the entire infrastructure.

* PAM Exploitation: Since the PAM system handles the injection of variables from /etc/environment, any misconfiguration in the PAM stack could lead to unauthorised environment manipulation before a user even reaches a functional prompt.

##  The Filesystem Hierarchy Standard

The ```Filesystem Hierarchy Standard``` (FHS), allowing users of other Linux distributions to easily find their way around Kali. The FHS defines the purpose of each directory. The top-level directories are described as follows:

* /bin/: basic programs.
* /boot/: Kali Linux kernel and other files required for its early boot process.
* /dev/: device files.
* /etc/: configuration files.
* //home/: user's personal files.
* /lib/: basic libraries.
* /media/: mount points for removable devices (CD/DVD-ROM, USB keys, and so on).
* /mnt/: temporary mount point.
* /opt/: extra applications provided by third parties.
* /root/: administrator's (root's) personal files.
* /run/: volatile runtime data that does not persist across reboots (not yet included in the FHS).
* /sbin/: system programs.
* /srv/: data used by servers hosted on this system.
* /tmp/: temporary files (this directory is often emptied at boot).
* /usr/: applications (this directory is further subdivided into bin, sbin, lib according to the same logic as in the root directory) Furthermore, /usr/share/ contains architecture-independent data. The /usr/local/ directory is meant to be used by the administrator for installing applications manually without overwriting files handled by the packaging system (dpkg).
* /var/: variable data handled by services. This includes log files, queues, spools, and caches.
* /proc/ and /sys/ are specific to the Linux kernel (and not part of the FHS). They are used by the kernel for exporting data to user space.

## The User's Home Directory

Traditionally, application configuration files are usually tucked away in your home directory as hidden "dotfiles," which stay out of sight unless you specifically ask your file manager or terminal to reveal them. While some programmes rely on a single hidden file, others create entire directories to organise their settings. However, because certain applications also use these folders to store extensive cached data, they can eventually take up a surprising amount of space on your hard drive.
Would you like some tips on how to find and tidy up these folders using the command line?

Historically, the sheer number of configuration files stored directly in the home directory—commonly known as ```dotfiles```—has led to a great deal of clutter. To address this, the XDG Base Directory Specification was introduced, establishing a cleaner convention where settings are tucked away in ~/.config, cache files in ~/.cache, and application data in ~/.local. Whilst this organised approach is gradually becoming the standard, users will still frequently encounter their desktop files in ~/Desktop/ and their incoming messages in the ~/Mail/ directory.

## Displaying and Modifying Text Files

To view a file's contents, you can use the ```cat``` command, although for longer documents, a pager like less or more is far more practical for reading page by page. When you need to create or modify text, editors such as Vi or Nano are the standard tools, yet simpler files can be generated directly through the terminal using redirection. By using the > operator, you can save a command's output into a new file, whereas the >> operator allows you to append new data to an existing file without overwriting what is already there.

```bash 
$ echo "Kali rules!" > kali-rules.txt
$ cat kali-rules.txt
Kali rules!
$ echo "Kali is the best!" >> kali-rules.txt
$ cat kali-rules.txt
Kali rules!
Kali is the best!
```

## Searching for Files and within Files

The find directory criteria command searches for files in the hierarchy under directory according to several criteria. The most commonly used criterion is ```-name filename``, which allows searching for a file by name. You can also use common wildcards such as "*"  in the filename search.

```bash
$ find /etc -name hosts
/etc/hosts
/etc/avahi/hosts
$ find /etc -name "hosts*"
/etc/hosts
/etc/hosts.allow
/etc/hosts.deny
/etc/avahi/hosts
```

The ```grep expression files``` command searches the contents of the files and extracts lines matching the regular expression. Adding the ```-r``` option enables a recursive search on all files contained in the directory. This allows you to look for a file when you only know a part of its contents.

##  Managing Processes

The ```ps aux```  command lists the processes currently running and helps to identify them by showing their PID. Once you know the PID of a process, the kill -signal pid command allows you to send it a signal (if you own the process). Several signals exist; most commonly used are ```TERM```  (a request to terminate gracefully) and ```KILL``` (a forced kill).

The command interpreter allows you to run programmes in the background simply by appending an ampersand (&) to your command, which lets you keep using the shell while the task carries on out of sight. You can keep track of these background tasks using the jobs command and, if necessary, bring one back to the foreground by typing fg ```%job-number```. If a programme is already running in the foreground, pressing ```Control+Z``` will pause it and return you to the command line, where you can then choose to resume it in the background using bg ```%job-number```.

##  Managing Rights

Linux is a multi-user system so it is necessary to provide a permissions system to control the set of authorized operations on files and directories, which includes all the system resources and devices (on a Unix system, any device is represented by a file or directory). This principle is common to all Unix-like systems.

Each file or directory has specific permissions for three categories of users:

    Its owner (symbolized by u, as in User).

    Its owner group (symbolized by g, as in Group), representing all the members of the group.

    The others (symbolized by o, as in Other).

Three types of rights can be combined:

    Reading (symbolized by r, as in Read).

    Writing (or modifying, symbolized by w, as in Write).

    Executing (symbolized by x, as in eXecute).

In the case of a file, these rights are easily understood: read access allows reading the content (including copying), write access allows changing it, and execute access allows running it (which will only work if it is a program).

## setuid and setgid executables

Executable files can be assigned two special permissions known as setuid and setgid, often referred to as "bits" because they represent simple on-off values. When a programme carries the s symbol in its permissions, it allows any user to run that specific file with the elevated privileges of the owner or the group, respectively. This clever mechanism is essential for granting temporary access to restricted system features that would otherwise be unavailable to a standard user.

Since a setuid root programme runs with the full authority of the super-user, it must be remarkably secure. If such a programme is compromised, it could allow a user to impersonate the root user and take total control of the system, which is why these files are frequently targeted for privilege escalation.On the other hand, the setgid bit is particularly clever when applied to directories. It ensures that any new file created within that folder automatically inherits the parent directory's group, rather than the user's primary group. This makes it an essential tool for collaboration, as it allows a team to work on shared files without constantly needing to fix group permissions.
* Summary of Special Permissions:
    - setuid (on files): Runs the programme with the permissions of the owner.

    - setgid (on files): Runs the programme with the permissions of the group.

    - setgid (on directories): Forces new files to inherit the folder's group ID.

    - Directory Basics: Remember that read allows listing files, write allows adding or deleting them, and execute is required to actually enter or "pass through" the directory using the cd command.


The sticky bit, represented by the letter "t", is a vital security feature for shared directories like /tmp/ where everyone has write access. It ensures that even if everyone can create files, only the original owner of a file (or the directory's owner) has the authority to delete it, preventing users from accidentally or maliciously removing each other's work. To manage these various permissions and ownership settings, three primary commands are used: chown to change the file's owner, chgrp to modify the associated group, and chmod to define the specific read, write, or execute rights.

* chown user file changes the owner of the file.
* chgrp group file alters the owner group.
* chmod rights file changes the permissions for the file.

### TIP Changing the user and groupTips

The symbolic representation of permissions is an intuitive method using letters and operators to define exactly who can do what with a file or directory. By using the categories u (owner), g (group), o (others), or a (all), you can precisely adjust rights without needing to remember complex numbers.

- Summary of Symbol
    * su/g/o/a: The target (User, Group, Others, or All).
    * +/-/=: The action (Add, Subtract, or Set explicitly).
    * r/w/x: The permission (Read, Write, or Execute).

### Examples
- chmod g+w report.txtAdds write permission for the group, leaving all other rights unchanged.

- ```chmod o-rwx``` private.shRemoves all permissions (read, write, execute) for others, effectively making the file private.

- ```chmod u=rwx``` script.shSets the owner's rights exactly to read, write, and execute, overwriting whatever was there before.

- ```chmod a=rx``` manual.pdfEnsures that everyone (all) has exactly read and execute access, but no one can modify the file.

The octal numeric representation is a concise way to set all file permissions at once by assigning a mathematical value to each right. You calculate the sum for each user category—owner, group, and others—resulting in a three or four-digit code. Unlike symbolic mode, this method completely overwrites existing permissions with the new total.

### The Value System4: 

- Read (r)2: 

- Write (w)1: Execute (x)

- 0: No permissions

### Examples 

* ```chmod 755``` script.shThe standard for programmes: the owner gets full access (4+2+1=7), while the group and others can only read and execute (4+1=5).

* ```chmod 644``` document.txtThe standard for data files: the owner can read and write (4+2=6), but everyone else can only read (4).

* ```chmod 600``` private.keyStrict privacy: the owner has read and write (6), but the group and others have no rights at all (00).

* ```chmod 4755``` system-toolUsing a fourth prefix digit sets special bits; here, the 4 at the start adds the setuid bit to the standard 755 permissions.

* ```chmod 2770``` shared-folderThis sets the setgid bit (2) on a folder where the owner and group have full control (77), but outsiders are locked out (0)


## Understanding the `umask` Command

The **umask** (user mask) is an octal value used to define the default permissions for newly created files and directories. It acts as a "filter" by **subtracting** specific rights from the system's initial default permissions to ensure new items aren't more accessible than intended.

### Key Concepts

*   **Restrictive Filter**: The mask defines which rights are **systematically removed** upon file creation.
*   **Automatic Removal**: If the system default is `666` and your umask is `022`, the system calculates `666 - 022` to result in `644`.
*   **Persistence**: To make a umask permanent for all your terminal sessions, you should add the command to your shell configuration file, such as `~/.bash_profile` or `~/.bashrc`.

---

### Examples

*   **`umask 022`**  
    The standard setting. It removes **write** access for the group and others.  
    *Result: New files are usually `644` (rw-r--r--) and directories `755` (rwxr-xr-x).*

*   **`umask 077`**  
    The "Private Mode" setting. It removes **all** rights for everyone except the owner.  
    *Result: New files are `600` (rw-------) and directories `700` (rwx------).*

*   **`umask 002`**  
    The "Collaborative" setting. It keeps write access for the group but removes it for others.  
    *Result: New files are `664` (rw-rw-r--) and directories `775` (rwxrwxr-x).*

*   **`umask`**  
    Running the command without arguments simply displays your **current mask** so you can verify your security settings.

## Recursive Operations and the "Special X"

When you need to adjust permissions for an entire folder and everything inside it, you use **recursive operations**. While the `-R` flag is powerful, it can be tricky when dealing with a mix of files and directories, which is where the uppercase **X** becomes essential.

### Key Concepts
*   **Recursive Flag (`-R`)**: Applying this option to `chmod`, `chown`, or `chgrp` forces the command to travel through every sub-directory and file in the tree.
*   **The Conditional Execute (`X`)**: Unlike the lowercase `x`, the uppercase **X** only applies the execute permission to **directories** or to files that **already have** at least one execute bit set.
*   **Smart Protection**: This prevents you from accidentally making every single text file or image "executable" just because you wanted to make the folders accessible.

### Examples

*   **`chmod -R 755 project_folder/`**  
    Changes the permissions for the folder and **every** file inside it to 755.  
    *Caution: This makes every regular file executable, which is often unwanted.*

*   **`chmod -R a+X project_folder/`**  
    Adds the execute right to all sub-directories (so you can `cd` into them) but **ignores** regular files like `.txt` or `.jpg`.

*   **`chown -R user:group backup/`**  
    Quickly changes the owner and group for a backup folder and the thousands of files contained within it.

*   **`chmod -R g-w,o-rwx private_data/`**  
    Recursively removes write access for the group and strips all rights from "others" for an entire project tree.


## Getting System Information and Logs

The free command displays information on memory; (df (for disk free*) reports on the available disk space on each of the disks mounted in the file system. Its -h option (for *human readable) converts the sizes into a more legible unit (usually mebibytes or gibibytes). In a similar fashion, the free command supports the -m and -g options, and displays its data either in mebibytes or in gibibytes, respectively.

```bash
$ free
              total        used        free      shared  buff/cache   available
Mem:        2052944      661232      621208       10520      770504     1359916
Swap:             0           0           0
$ df
Filesystem     1K-blocks     Used Available Use% Mounted on
udev             1014584        0   1014584   0% /dev
tmpfs             205296     8940    196356   5% /run
/dev/vda1       30830588 11168116  18073328  39% /
tmpfs            1026472      456   1026016   1% /dev/shm
tmpfs               5120        0      5120   0% /run/lock
tmpfs            1026472        0   1026472   0% /sys/fs/cgroup
tmpfs             205296       36    205260   1% /run/user/132
tmpfs             205296       24    205272   1% /run/user/0
```


The id command displays the identity of the user running the session along with the list of groups they belong to. 

```bash
$ id
uid=1000(kali) gid=1000(kali) groups=1000(kali),27(sudo)
```

## System Identity and Diagnostic Commands

To manage a system effectively, you must be able to identify your current permissions and understand the underlying hardware and kernel. The following commands provide essential run-time data and system logs for troubleshooting and reporting.

### Key Commands
*   **User Identity (`id`)**: Shows your unique User ID (UID), primary Group ID (GID), and all supplementary groups you belong to. This is vital for verifying if you have the necessary group memberships to access specific files or devices.
*   **System Overview (`uname -a`)**: Provides a detailed summary of your system, including the kernel version, architecture (e.g., x86_64), and hostname. This information is a standard requirement when submitting bug reports.
*   **Kernel Logs (`dmesg`)**: Retrieves messages from the kernel's ring buffer. It is the go-to tool for seeing "live" hardware events, such as connecting a USB drive or identifying hardware failures during boot.

---

### Examples

*   **`id`**  
    Check your current identity.  
    *Example Output: `uid=1000(user) gid=1000(user) groups=1000(user),27(sudo)` — indicates you have administrative (sudo) privileges.*

*   **`uname -a`**  
    Print all system information.  
    *Use this to confirm if you are running a 64-bit kernel or to check your exact Linux version for software compatibility.*

*   **`dmesg | tail -n 20`**  
    View the last 20 lines of the kernel log.  
    *Perfect for checking what happened immediately after plugging in a new piece of hardware.*

*   **`dmesg -w`**  
    Follow the kernel logs in real-time.  
    *Useful for monitoring the system as you perform actions like inserting a network cable or a disk.*

## Managing Logs with `journalctl`

The **systemd journal** acts as a centralised storage for various system logs, including service output (stdout/stderr), syslog messages, and kernel logs. The `journalctl` command is the primary tool used to query and filter these logs efficiently.

### Key Features

*   **Centralised Logging**: Collects logs from nearly every part of the system into a single database.
*   **Chronological Order**: By default, it displays logs from the oldest to the newest, but this can be easily reversed.
*   **Live Monitoring**: Similar to `dmesg`, it can follow logs in real-time as they are generated.
*   **Targeted Filtering**: It allows you to isolate logs from a specific service or "unit," which is essential for troubleshooting broken applications.

---

### Examples

*   **`journalctl`**  
    Dumps all stored logs into a pager (like `less`) for manual browsing.

*   **`journalctl -r`**  
    Shows the **most recent** logs first. This is usually the first command you run when something has just gone wrong.

*   **`journalctl -f`**  
    "Follows" the logs. The terminal stays open and prints new messages the moment they happen.

*   **`journalctl -u ssh.service`**  
    Filters logs to show **only** those related to the SSH service. This is perfect for identifying failed login attempts.

*   **`journalctl -p err`**  
    A useful extra: this filters the journal to show only messages with a priority of **"error"** or higher.

## Discovering the Hardware

The Linux kernel exports detailed hardware information through the /proc/ and /sys/ virtual filesystems, which can be queried using tools like lspci (pciutils) and lsusb (usbutils) for identification. These tools, along with lspcmcia (pcmciautils), facilitate precise hardware model identification to aid in finding relevant online documentation

* Example of information provided by lspci and lsusb

```bash 
$ lspci
[...]
00:02.1 Display controller: Intel Corporation Mobile 915GM/GMS/910GML Express Graphics Controller (rev 03)
00:1c.0 PCI bridge: Intel Corporation 82801FB/FBM/FR/FW/FRW (ICH6 Family) PCI Express Port 1 (rev 03)
00:1d.0 USB Controller: Intel Corporation 82801FB/FBM/FR/FW/FRW (ICH6 Family) USB UHCI #1 (rev 03)
[...]
01:00.0 Ethernet controller: Broadcom Corporation NetXtreme BCM5751 Gigabit Ethernet PCI Express (rev 01)
02:03.0 Network controller: Intel Corporation PRO/Wireless 2200BG Network Connection (rev 05)
$ lsusb
Bus 005 Device 004: ID 413c:a005 Dell Computer Corp.
Bus 005 Device 008: ID 413c:9001 Dell Computer Corp.
Bus 005 Device 007: ID 045e:00dd Microsoft Corp.
Bus 005 Device 006: ID 046d:c03d Logitech, Inc.
[...]
Bus 002 Device 004: ID 413c:8103 Dell Computer Corp. Wireless 350 Bluetooth
```
These programs have a -v option that lists much more detailed (but usually unnecessary) information. Finally, the ```lsdev``` command (in the procinfo package) lists communication resources used by devices.

The ```lshw``` program is a combination of the above programs and displays a long description of the hardware discovered in a hierarchical manner. You should attach its full output to any report about hardware support problems.

# Linux Command Breakdown

Here is a detailed breakdown of each command mentioned in the text, including its primary purpose and function.

### Navigation and File Management
*   **`pwd`**: Prints the full path of the current working directory.
*   **`cd`**: Changes the current directory to a new specified location.
*   **`ls`**: Lists the contents of a directory, such as files and sub-folders.
*   **`mkdir`**: Creates a new, empty directory.
*   **`rmdir`**: Removes an empty directory.
*   **`mv`**: Moves or renames files and directories.
*   **`rm`**: Deletes files or directories from the system.
*   **`cp`**: Copies files or directories from one location to another.

### File Viewing and Editing
*   **`cat`**: Concatenates and displays the entire content of a file to the terminal.
*   **`less`**: A "pager" that allows you to view file contents one page at a time.
*   **`more`**: An older pager used to view text files screen by screen.
*   **`editor`**: A generic command that launches a text editor like Nano or Vi.
*   **`find`**: Searches for files or directories within a file tree based on specific criteria.

### System Monitoring and Logging
*   **`free`**: Displays the amount of free and used memory (RAM) in the system.
*   **`df`**: Reports the amount of available disk space on file systems.
*   **`id`**: Displays the current user's identity, including UID, GID, and groups.
*   **`dmesg`**: Prints the message buffer of the kernel, useful for hardware diagnostics.
*   **`journalctl`**: Queries and displays logs from the systemd journal database.

### Hardware Discovery
*   **`lspci`**: Lists all PCI devices, such as graphics cards and network adapters.
*   **`lsusb`**: Lists all USB devices currently connected to the machine.
*   **`lspcmcia`**: Lists PCMCIA cards, typically used in older laptop hardware.

### Process Management
*   **`ps`**: Provides a snapshot of the current running processes.
*   **`kill`**: Sends a signal to a process, usually to terminate it.
*   **`bg`**: Resumes a suspended job by running it in the background.
*   **`fg`**: Brings a background process to the foreground to interact with it.
*   **`jobs`**: Lists the active jobs started in the current shell session.

### Permissions and Ownership
*   **`chmod`**: Changes the access permissions (read, write, execute) of a file or directory.
*   **`chown`**: Changes the owner of a specific file or directory.
*   **`chgrp`**: Changes the group ownership of a file or directory.

