# Running a Flask based website on Nginx

This article assumes you have completed up to setting up Nginx based on the [Last Article](/articles/rpilinuxserver/), or that you already have a server setup.

## Configuring Nginx

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
        server_name example.com www.example.com;

        location / {
                proxy_pass http://127.0.0.1:8000/;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header X-Forwarded-Host $host;
                proxy_set_header X-Forwarded-Prefix /;
        }
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

## Running the Flask App

### Install Gunicorn

To run the your Flask website you need to install gunicorn.

<pre><code>
pip install gunicorn
sudo cp ~/.local/bin/gunicorn /usr/bin/gunicorn
</pre></code>

### Configure Systemd

You will need to create a systemd service for gunicorn.

In `/etc/systemd/system/yourapp.service`

<pre><code>
[Unit]
Description = yourapp
After = network.target

[Service]
PermissionsStartOnly = true
PIDFile = /run/yourapp/yourapp.pid
User = gunicorn
Group = gunicorn
WorkingDirectory = /var/www/yourapp
ExecStartPre = /bin/mkdir /run/yourapp
ExecStartPre = /bin/chown -R gunicorn:gunicorn /run/yourapp
ExecStart = /usr/bin/gunicorn main:app -b 0.0.0.0:8000 --pid /run/yourapp/yourapp.pid
ExecReload = /bin/kill -s HUP $MAINPID
ExecStop = /bin/kill -s TERM $MAINPID
ExecStopPost = /bin/rm -rf /run/yourapp
PrivateTmp = true

[Install]
WantedBy = multi-user.target
</pre></code>

Now you will need to run the following commands:

<pre><code>
sudo systemctl daemon-reload
sudo systemctl enable yourapp
sudo systemctl start yourapp

sudo setsebool -P httpd_can_network_connect 1
</pre></code>

At this point when you navigate to your website, it should load.

## Installing and Running Certbot

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

