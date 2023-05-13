FROM nginx:1.23.4

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./assets/config.ndjson /assets/
COPY import-dashboard.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/import-dashboard.sh

CMD ["/bin/sh", "-c", "/usr/local/bin/import-dashboard.sh && nginx -g 'daemon off;'"]