FROM odoo:18.0

COPY ./odoo.conf /etc/odoo/odoo.conf

WORKDIR /usr/lib/python3/dist-packages/odoo

EXPOSE 8069

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
