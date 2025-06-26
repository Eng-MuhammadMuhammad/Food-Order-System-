FROM odoo:18.0
COPY ./docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
WORKDIR /usr/lib/python3/dist-packages/odoo
EXPOSE 8069
ENTRYPOINT ["docker-entrypoint.sh"]
