# Hosting a Website on the Raspberry Pi with Rocky Linux

First Download Rocky Linux for the Raspberry Pi 3 & 4 from
[their website](https://rockylinux.org/alternative-images).

<center>
![Screen Shot 2022-02-19 at 2.15.13 PM](/articles/rpilinuxserver/img/ScreenShot2022-02-19at2.15.13PM.png)
</center>

Next you want to burn this image to the sd card that you are going to use. Now
start up the Raspberry Pi and login with the default user `rocky` and the
password is `rockylinux`.

To make the image take up the whole drive, run:

<pre><code>
sudo rootfs-expand
</pre></code>

Now, you should create a new user:

<pre><code>
sudo useradd -m -g users -G wheel userName
sudo passwd username
</pre></code>

Next, we should delete the default user so logout and login to your new user:

<pre><code>
sudo userdel rocky
</pre></code>



***

## Setting a static IP address

The easiest way is to run:

<pre><code>
sudo nmtui
</pre></code>

<center>
![Screen Shot 2022-02-19 at 2.18.39 PM](/articles/rpilinuxserver/img/ScreenShot2022-02-19at2.18.39PM.png)
</center>

Select **Edit** a connection and select your network interface.

<center>
![Screen Shot 2022-02-19 at 2.23.20 PM](/articles/rpilinuxserver/img/ScreenShot2022-02-19at2.23.20PM.png)
</center>

Select **Show** for **IPv4 CONFIGURATION** and enter the IP you want to set.
Then select **OK** at the bottom, and quit the program.

## Securing the PI

### SSH Key Authorization

The best way to secure the pi is to use an SSH key to login instead of a
password. First you want to generate an SSH key by running on your computer:

<pre><code>
ssh-keygen -t rsa
</pre></code>

Next, to copy your SSH key to your server, run:

<pre><code>
ssh-copy-id -i ~/.ssh/mykey user@host
</pre></code>

To test that it works, run:

<pre><code>
ssh -i ~/.ssh/mykey user@host
</pre></code>

If it worked, you should be able to connect without needing a password.

To force an SSH key to login, edit `/etc/ssh/sshd_config` using nano or vim.

Change

<pre><code>
PermitRootLogin yes
PasswordAuthentication yes
</code></pre>
to
<pre><code>
PermitRootLogin no
PasswordAuthentication no
</pre></code>

### Setting up fail2ban

First start and enable firewalld to run at boot:

<pre><code>
sudo systemctl start firewalld
sudo systemctl enable firewalld
</pre></code>

Now, enable the EPEL repository for Rocky Linux and install fail2ban:

<pre><code>
sudo dnf install epel-release -y
sudo dnf install fail2ban fail2ban-firewalld -y
</pre></code>

Start and enable fail2ban to run at boot:

<pre><code>
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
</pre></code>

Now, we have to make fail2ban work with firewalld, run:

<pre><code>
sudo mv /etc/fail2ban/jail.d/00-firewalld.conf /etc/fail2ban/jail.d/00-firewalld.local
sudo systemctl restart fail2ban
</pre></code>

To create an SSH jail, edit the ssh config file with nano or vim:

<pre><code>
sudo nano /etc/fail2ban/jail.d/sshd.local
</pre></code>

Paste the following into the file and change the values as you see fit:

<pre><code>
[sshd]
enabled = true
bantime = 1d
maxretry = 3
</pre></code>

Save and close the file and restart fail2ban:

<pre><code>
sudo systemctl restart fail2ban
</pre></code>

## Setting up Dynamic DNS with Google Domains

### Configuring Google Domains

First, on [Domains.google.com](https://domains.google.com/) go the DNS page for
your domain. Scroll down and click on **Show advanced settings**, Click **Manage
dynamic DNS**, and then click **Create new record**. Enter your subdomain or
leave it black for the domain itself. Finally, click Save.

### Installing ddclient

To install ddclient you need to enable the PowerTools Repo for the perl
dependency.

First, install `dnf-plugins-core`:

<pre><code>
sudo dnf -y install dnf-plugins-core
sudo dnf upgrade
</pre></code>

Next, enable PowerTools:

<pre><code>
sudo dnf config-manager --set-enabled powertools
</pre></code>

Then, you can install ddclient:

<pre><code>
sudo dnf install ddclient
</pre></code>

Now, we want to edit the config file for ddclient:

<pre><code>
sudo nano /etc/ddclient.conf
</pre></code>

You'll want to look for where it says `protocol=dyndns2`, and enter your
information:

<pre><code>
##
## nsupdate.info IPV4(https://www.nsupdate.info)
##
protocol=dyndns2
use=web, web=http://ipv4.nsupdate.info/myip
server=domains.google.com
login=username
password=password
domain.tld
</pre></code>

Wait about 5 minutes and on the Google Domains website, under Dynamic DNS you
should see your IP address under **Data**.

## Setting up NGINX and Let's Encrypt

### Installing NGINX

First, install nginx Webserver:

<pre><code>
sudo dnf install nginx
</pre></code>

Next, start and enable nginx to run at boot:

<pre><code>
sudo systemctl start nginx
sudo systemctl enable nginx
</pre></code>

Then, check the status to see if it is running:

<pre><code>
sudo systemctl status nginx
</pre></code>

<center>
![Screen Shot 2022-02-19 at 2.56.21 PM](/articles/rpilinuxserver/img/ScreenShot2022-02-19at2.56.21PM.png)
</center>

Now, we have to allow HTTP traffic through the firewall:

<pre><code>
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --reload
</pre></code>

In a web browser, go to the local ip of the server and you should see the nginx
welcome page.

<center>
![Screen Shot 2022-02-19 at 2.58.29 PM](/articles/rpilinuxserver/img/ScreenShot2022-02-19at2.58.29PM.png)
</center>

### Configuring NGINX

First, make your folder for the website, this is where your website will live:

<pre><code>
sudo mkdir -p /var/www/websiteName
</pre></code>

Next, we need to set the proper permissions to make sure everything works:

<pre><code>
sudo chown -R nginx /var/www/websiteName
sudo chmod -R 755 /var/www/websiteName
</pre></code>

Now, we will create the config file for website:

<pre><code>
sudo nano /etc/nginx/conf.d/websiteName.conf
</pre></code>

and paste the following into the file:

<pre><code>
server {
    listen 80;
    server_name domain.tld www.domain.tld;
    root /var/www/websiteName;
    index index.php index.html index.htm;
    access_log /var/log/nginx/websiteName.access.log;
    error_log /var/log/nginx/websiteName.error.log;
}
</pre></code>

Now, confirm that the nginx configuration is ok:

<pre><code>
sudo nginx -t
</pre></code>

Restart nginx:

<pre><code>
sudo systemctl restart nginx
sudo systemctl status nginx
</pre></code>

Next, set SELinux to permissive mode:

<pre><code>
sudo setenforce permissive
sudo getenforce
</pre></code>

Now, we will need to set SELinux to permissive mode permanently:

<pre><code>
sudo sed -i --follow-symlinks 's/SELINUX=enforcing/SELINUX=permissive/g' /etc/sysconfig/selinux
</pre></code>

### Installing and Running Certbot

To install Certbot run:

<pre><code>
sudo dnf install certbot python3-certbot-nginx
</pre></code>

To get SSL certificates for your websites run:

<pre><code>
sudo certbot --nginx
</pre></code>

Answer the prompts that show up on screen as you wish.

To configure auto renewal of the SSL certificate run:

<pre><code>
crontab -e
</pre></code>

and add the following line:

<pre><code>
0 12 * * * /usr/bin/certbot renew --quiet
</pre></code>

This will check everyday at noon to see if the certificate will expire in the
next month, if so it will renew the certificate.

Now your website should be operational.

