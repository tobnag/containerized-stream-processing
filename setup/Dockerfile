ARG ELASTIC_VERSION

FROM elasticsearch:${ELASTIC_VERSION}

# The 'setup' service runs a one-off script which initializes users inside
# Elasticsearch — such as 'logstash_internal' and 'kibana_system' — with the
# values of the passwords defined in the '.env' file.
#
# This task is only performed during the *initial* startup of the stack. On all
# subsequent runs, the service simply returns immediately, without performing
# any modification to existing users.

USER root

RUN set -eux; \
	mkdir /state; \
	chmod 0775 /state; \
	chown elasticsearch:root /state

USER elasticsearch:root

ENTRYPOINT ["/entrypoint.sh"]
