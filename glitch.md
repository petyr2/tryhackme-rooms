# This is a webapp-based room where we are going to look at Node Deserialization

In Node.js, deserialization usually means taking input (often JSON or objects) and turning it back into a JavaScript object using a library such as:

JSON.parse() (safe if used properly), or packages like node-serialize, which in older versions could deserialize not only data but also functions.

In this room, we shall be playing with api's and such.

# Let's see how APIs work before we even start with our room.

Suppose we visit a movie rental site that communicates with its backend using an API.

If we want to see what movies are available, we make a GET request:

Variable: genre

Value: comedy

Meaning: “Show me all comedy movies.”

The API responds with a list of comedy movies in stock.

If we want to add a new movie review, we make a POST request:

Variable: review

Value: “This movie was amazing!”

Meaning: “Store this new review in the system.”

The API processes it and saves our review in the database.

Since we have a basic understanding of the APIs, we can move on to attacking the room

We shall start with a basic nmap scan `nmap -A 10.10.204.13` found port 80 open

Also, we do some directory brute forcing using gobustor.`gobuster dir -u http://10.10.204.13 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt`

Upon viewing the page source, I found a path to `/api/access`, and when I visited the path found some token that are in base 64 encoding.

Let's decode the tokens and potentially see the content in it. After decoding it, you get the first flag. `echo -n "dGhpc19pc19ub3RfcmVhbA==" | base64 --decode`

Decoded string update it to the token and then refresh the page, and boom, the page changes. Since the page has nothing interesting, we can view the page source and the page source,

<img width="480" height="270" alt="Screenshot From 2025-08-18 02-43-46" src="https://github.com/user-attachments/assets/a3c0868a-9aaf-4c5c-9300-26a25327ac6b" />

We can see there is a .js file, which, upon opening it, I found a script with a path that we can visit

<img width="759" height="596" alt="Screenshot From 2025-08-18 02-44-47" src="https://github.com/user-attachments/assets/19ee6516-42f8-4b13-b309-a57d232769be" />

Since on the path there isn't anything that could help us, and on the hint section it says What other methods does the API accept? Let's use Burp and see what we can do with it.

On burp, we found that we can use some options to play along with the path.

<img width="1112" height="304" alt="Screenshot From 2025-08-18 02-55-09" src="https://github.com/user-attachments/assets/cae4cbf8-a0b3-4de2-919e-4f7618899b36" />

Upon using a POST request, I found this message.

<img width="1164" height="305" alt="Screenshot From 2025-08-18 03-15-42" src="https://github.com/user-attachments/assets/a9264616-9673-4c09-884a-b469b6f1aafa" />

In order to identify what parameter to use in this, we can fuzz for a parameter using gobuster or wfuzz.

```bash
gobuster fuzz -m POST -u http://10.10.204.13/api/items?FUZZ=test -w Seclists/Discovery/Web-Content/api/objects.txtgobuster fuzz -u "http://10.10.204.13/api/items?FUZZ=test" \
-w /usr/share/seclists/Discovery/Web-Content/api/objects.txt \
--method POST
````

<img width="766" height="168" alt="Screenshot From 2025-08-18 03-17-54" src="https://github.com/user-attachments/assets/c125318f-770f-4c32-a72d-314fd892cc9f" />

using wfuzz
```bash
wfuzz -c -z file,/usr/share/wordlists/wfuzz/general/common.txt -X POST --hh 45 -u http://10.10.204.13/api/items\?FUZZ\=dfr
```
<img width="958" height="310" alt="Screenshot From 2025-08-18 03-24-08" src="https://github.com/user-attachments/assets/9556c66c-726a-4171-a3c0-c0f5d66d1c17" />

The parameter to use is cmd, which, after sending the request again on Burp it returned an error.

<img width="1510" height="664" alt="Screenshot From 2025-08-18 03-27-29" src="https://github.com/user-attachments/assets/0052b4f9-6190-44c5-8305-c5f6bb344dbb" />

At this point, we need to access a shell so that we can solve the other problems.















































































