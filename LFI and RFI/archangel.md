# In this room, we are going to look into LFI.

We perform an nmap scan where we see that ports 22 and 80 are open.

Also, we access the site and see that there is a website that is running on the site. We can see an email section that reveals another hostname that we can use since nothing interesting on our current site.

Before visiting the site, you must add to the `/etc/hosts` file. Upon visiting the site, I did some dirsearch on the site and found a `test.php` directory, which can also be seen when we visit the `robots.txt`

When I visited the directory, I found that it was redirecting me to another file. This indicates that there is locoal file inclusion vulnerability available on the site.

<img width="871" height="233" alt="Screenshot From 2025-08-29 22-22-12" src="https://github.com/user-attachments/assets/5106905d-6241-44f3-952a-6ef03ee4c140" />


