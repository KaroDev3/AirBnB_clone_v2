#!/usr/bin/env bash
# script that sets up the web servers for the deployment of web_static

# Install Nginx if it not already installed
if ! which nginx > /dev/null 2>&1; then
    sudo apt-get -y update
    sudo apt-get install -y nginx
fi

# Create the folder /data/web_static/releases/test/
mkdir -p /data/web_static/releases/test/

# Create the folder /data/web_static/shared/
mkdir -p /data/web_static/shared/

# Create a fake HTML file /data/web_static/releases/test/index.html
printf %s "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" > /data/web_static/releases/test/index.html

# symbolic link to /data/web_static/releases/test/
ln -sf /data/web_static/releases/test /data/web_static/current


# Give ownership of the /data/ folder to the ubuntu user AND group
chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/
# to hbnb_static (ex: https://mydomainname.tech/hbnb_static).
new_string="\\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sed -i "29i $new_string" /etc/nginx/sites-enabled/default

# restart nginx
service nginx restart
