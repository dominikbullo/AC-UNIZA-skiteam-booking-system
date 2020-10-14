# Hosting multiple SSL-enabled sites with Docker and Nginx

### Getting set up
```
$ mkdir nginx-proxy && cd nginx-proxy
$ docker network create nginx-proxy
```
## Creating the docker-compose-base.yml file

```
version: '3'

services:
  nginx:
    image: nginx:1.13.1
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - conf:/etc/nginx/conf.d
      - vhost:/etc/nginx/vhost.d
      - html:/usr/share/nginx/html
      - certs:/etc/nginx/certs
    labels:
      - "com.github.jrcs.letsencrypt_nginx_proxy_companion.nginx_proxy=true"

  dockergen:
    image: jwilder/docker-gen:0.7.3
    container_name: nginx-proxy-gen
    depends_on:
      - nginx
    command: -notify-sighup nginx-proxy -watch -wait 5s:30s /etc/docker-gen/templates/nginx.tmpl /etc/nginx/conf.d/default.conf
    volumes:
      - conf:/etc/nginx/conf.d
      - vhost:/etc/nginx/vhost.d
      - html:/usr/share/nginx/html
      - certs:/etc/nginx/certs
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - ./nginx.tmpl:/etc/docker-gen/templates/nginx.tmpl:ro

  letsencrypt:
    image: jrcs/letsencrypt-nginx-proxy-companion
    container_name: nginx-proxy-le
    depends_on:
      - nginx
      - dockergen
    environment:
      NGINX_PROXY_CONTAINER: nginx-proxy
      NGINX_DOCKER_GEN_CONTAINER: nginx-proxy-gen
    volumes:
      - conf:/etc/nginx/conf.d
      - vhost:/etc/nginx/vhost.d
      - html:/usr/share/nginx/html
      - certs:/etc/nginx/certs
      - /var/run/docker.sock:/var/run/docker.sock:ro

volumes:
  conf:
  vhost:
  html:
  certs:

# Do not forget to 'docker network create nginx-proxy' before launch, and to add '--network nginx-proxy' to proxied containers. 

networks:
  default:
    external:
      name: nginx-proxy
```

```
$ docker-compose up -d
```

The process will start by downloading a few Docker images, and if things finish successfully, the output will end with the following:

## ARM FIX
https://github.com/nginx-proxy/nginx-proxy/pull/1071

```
$ docker-compose -f docker-compose-arm.yml up -d
```

```console
Creating nginx-proxy ...
Creating nginx-proxy ... done
Creating nginx-proxy-gen ...
Creating nginx-proxy-gen ... done
Creating nginx-proxy-le ...
Creating nginx-proxy-le ... done
To confirm this, run docker ps. You should see three running containers, named nginx-proxy, nginx-proxy-gen, and nginx-proxy-le, like this:
```
```console
CONTAINER ID        IMAGE                                    COMMAND                  CREATED             STATUS              PORTS                                      NAMES
9ea5fffc24dd        jrcs/letsencrypt-nginx-proxy-companion   "/bin/bash /app/en..."   4 minutes ago       Up 4 minutes                                                   nginx-proxy-le
e2288dfc3c5c        jwilder/docker-gen:0.7.3                 "/usr/local/bin/do..."   4 minutes ago       Up 3 seconds                                                   nginx-proxy-gen
eda8f12bd829        nginx:1.13.1                             "nginx -g 'daemon ..."   4 minutes ago       Up 4 minutes        0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp   nginx-proxy
```
If any of those aren’t running, you should check their logs. You can do that with docker logs.

```
$ docker logs nginx-proxy
$ docker logs nginx-proxy-gen
$ docker logs nginx-proxy-le
```

I’ve found that most issues arise from nginx-proxy-gen. If you see an error about the nginx-proxy network, try creating the network again with docker network create nginx-proxy. If there are issues with the nginx.tmpl file, double check that it’s the same as the one on Github.

If your three containers are running smoothly, then you’re ready to start deploying other SSL-enabled containers behind the proxy! At this point, we’re shifting away from configuring nginx-proxy and toward the ways, you should configure your apps to run behind it.

Step 4. Set up your DNS
Let’s Encrypt will only issue certificates to real domains, not IPs. In order to receive valid certificates, you must set up your DNS correctly. Most likely, you will find your DNS settings with the company from which you bought your domain.

Let’s say I want to run Miniflux, a self-hosted RSS reader, on the feeds.example.com domain. In my DNS settings, I would create a new A record that directs feeds.example.com to the public IP of the VPS where I set up my nginx-proxy.

This is not an optional step. Valid, reachable domains are required for SSL to work.

Quick tip: to find your VPSs’ public IP, use the following: dig +short myip.opendns.com @resolver1.opendns.com.

Step 5. The configuration basics
In order to set up any containerized app to work with this beautiful proxy we’ve now set up, you must configure the following:

Three environment variables: VIRTUAL_HOST, LETSENCRYPT_HOST, LETSENCRYPT_EMAIL
The Docker network (nginx-proxy)
Exposing port 80/443
Environment variables
Here are the environment variables:

VIRTUAL_HOST
LETSENCRYPT_HOST
LETSENCRYPT_EMAIL
The VIRTUAL_HOST and LETSENCRYPT_HOST variables will be the same for almost all applications, and will correspond to the domain you used in the previous step to set up DNS.

The LETSENCRYPT_EMAIL variable is self-explanatory: use the email address of your choosing.

Let’s extend our example from the last step. Here’s the docker-compose settings I would use for that Miniflux installation, given that my email is foo@example.com:

environment:
    VIRTUAL_HOST: feeds.example.com
    LETSENCRYPT_HOST: feeds.example.com
    LETSENCRYPT_EMAIL: foo@example.com
Docker network
This will be nginx-proxy, unless you changed it. Here’s how it looks in a docker-compose.yml file:

networks:
  default:
    external:
      name: nginx-proxy
Expose port(s)
Any container you create must expose the port on which it listens to traffic. That will be 80, 443, or both. Here’s how it looks in a docker-compose.yml file:

expose:
  - 80
A example configuration
And here’s how all those different variables and configurations look like in a very basic docker-compose.yml file.

version: '3'

services:
  example-app:
    image: example/example-app
    expose:
      - 80
    environment:
      VIRTUAL_HOST: app.example.com
      LETSENCRYPT_HOST: app.example.com
      LETSENCRYPT_EMAIL: foo@example.com

networks:
    default:
        external:
            name: nginx-proxy
At this point, you should have everything you need to know to deploy all kinds of Docker containers under this SSL-enabled proxy. Let’s look at a few examples to show you how it works in the real world.

Leading by example: Miniflux
Remember how I wanted to self-host Miniflux at the feeds.example.com domain? Here’s the docker-compose.yml that I came up with. Note the expose, environment, and networks configurations.

version: '2'

services:
  miniflux:
    image: miniflux/miniflux:latest
    expose:
      - 80
    volumes:
      - miniflux_data:/var/www/html/data
    environment:
      VIRTUAL_HOST: feeds.example.com
      LETSENCRYPT_HOST: feeds.example.com
      LETSENCRYPT_EMAIL: foo@example.com

volumes:
  miniflux_data:
        driver: local

networks:
    default:
        external:
            name: nginx-proxy
Initialize the container with docker-compose up -d and you’ll have an SSL-enabled feed reader in about 30 seconds!

Leading by example, take 2: WordPress
In my previous tutorial on nginx-proxy, I showed off how easy it is to launch a WordPress instance running behind the proxy.

It’s just as easy to do it with SSL. I took the exact same docker-compose.yml file and simply added the LETSENCRYPT_HOST and LETSENCRYPT_EMAIL environment variables. You have to change those two fields according to your needs, in addition to VIRTUAL_HOST.

Take note of the db_node_domain field below. This is where you specify the name of the database that WordPress will connect to. Keep in mind that these names should be unique for each instance of WordPress, and you need to also change the depends_on: and WORDPRESS_DB_HOST: fields accordingly.

version: "3"

services:
   db_node_domain:
     image: mysql:5.7
     volumes:
        - db_data:/var/lib/mysql
     restart: always
     environment:
        MYSQL_ROOT_PASSWORD: somewordpress
        MYSQL_DATABASE: wordpress
        MYSQL_USER: wordpress
        MYSQL_PASSWORD: wordpress
     container_name: wp_test_db

   wordpress:
     depends_on:
        - db_node_domain
     image: wordpress:latest
     expose:
        - 80
     restart: always
     environment:
        VIRTUAL_HOST: blog.example.com
        LETSENCRYPT_HOST: blog.example.com
        LETSENCRYPT_EMAIL: foo@example.com
        WORDPRESS_DB_HOST: db_node_domain:3306
        WORDPRESS_DB_USER: wordpress
        WORDPRESS_DB_PASSWORD: wordpress
     container_name: wp_test
volumes:
  db_data:

networks:
  default:
    external:
      name: nginx-proxy
Run it with docker-compose up -d and then visit your domain—there’s that beautiful WordPress installation page with SSL encryption.

Sweet.

Wrapping up
This has been a pretty extensive tutorial, so I understand if you’re feeling a little overwhelmed. My goal here isn’t to guide you toward any specific end goal, but rather to give you the tools to leverage the fantastic nginx-proxy project to your unique needs.

If you keep the required settings in mind, you should be able to put almost any containerized app behind this proxy. And that gives you a ton of power to get the most out of your VPS.

Best of all, docker-letsencrypt-nginx-proxy-companion will automatically renew your certificates for you, so there’s no need to check in or do any manual interventions.

As far as I can tell, this is the best way to serve many, if not dozens of SSL-encrypted websites and apps via a single proxy and a single VPS.

[cta text=”Run Docker for $1.11/mo and get 16GB RAM!” text2=”You’re 90 seconds away from running Docker with multiple websites on SSD Nodes!” button=”Start Dockerizing your apps”]

## Code Samples



