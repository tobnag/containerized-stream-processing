FROM alpine:3.17.3

RUN apk update && \
    apk add --no-cache curl

COPY ./assets/dashboard.ndjson /assets/
COPY import-dashboard.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/import-dashboard.sh

CMD ["/usr/local/bin/import-dashboard.sh"]