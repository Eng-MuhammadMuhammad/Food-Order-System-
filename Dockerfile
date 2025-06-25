FROM odoo:16.0  # or your preferred Odoo version

# Optional: copy custom addons or config
# COPY ./addons /mnt/extra-addons
# COPY ./odoo.conf /etc/odoo/

# Set working directory
WORKDIR /usr/lib/python3/dist-packages/odoo

# Expose Odoo default port
EXPOSE 8069

# Start Odoo
CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
