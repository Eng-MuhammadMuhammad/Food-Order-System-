FROM odoo:18.0

WORKDIR /usr/lib/python3/dist-packages/odoo

EXPOSE 8069

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
