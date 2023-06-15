Apache + mod-wsgi configuration
===============================

An example Apache2 vhost configuration follows::

    WSGIDaemonProcess wagtailblog-<target> threads=5 maximum-requests=1000 user=<user> group=staff
    WSGIRestrictStdout Off

    <VirtualHost *:80>
        ServerName my.domain.name

        ErrorLog "/srv/sites/wagtailblog/log/apache2/error.log"
        CustomLog "/srv/sites/wagtailblog/log/apache2/access.log" common

        WSGIProcessGroup wagtailblog-<target>

        Alias /media "/srv/sites/wagtailblog/media/"
        Alias /static "/srv/sites/wagtailblog/static/"

        WSGIScriptAlias / "/srv/sites/wagtailblog/src/wagtailblog/wsgi/wsgi_<target>.py"
    </VirtualHost>


Nginx + uwsgi + supervisor configuration
========================================

Supervisor/uwsgi:
-----------------

.. code::

    [program:uwsgi-wagtailblog-<target>]
    user = <user>
    command = /srv/sites/wagtailblog/env/bin/uwsgi --socket 127.0.0.1:8001 --wsgi-file /srv/sites/wagtailblog/src/wagtailblog/wsgi/wsgi_<target>.py
    home = /srv/sites/wagtailblog/env
    master = true
    processes = 8
    harakiri = 600
    autostart = true
    autorestart = true
    stderr_logfile = /srv/sites/wagtailblog/log/uwsgi_err.log
    stdout_logfile = /srv/sites/wagtailblog/log/uwsgi_out.log
    stopsignal = QUIT

Nginx
-----

.. code::

    upstream django_wagtailblog_<target> {
      ip_hash;
      server 127.0.0.1:8001;
    }

    server {
      listen :80;
      server_name  my.domain.name;

      access_log /srv/sites/wagtailblog/log/nginx-access.log;
      error_log /srv/sites/wagtailblog/log/nginx-error.log;

      location /500.html {
        root /srv/sites/wagtailblog/src/wagtailblog/templates/;
      }
      error_page 500 502 503 504 /500.html;

      location /static/ {
        alias /srv/sites/wagtailblog/static/;
        expires 30d;
      }

      location /media/ {
        alias /srv/sites/wagtailblog/media/;
        expires 30d;
      }

      location / {
        uwsgi_pass django_wagtailblog_<target>;
      }
    }
