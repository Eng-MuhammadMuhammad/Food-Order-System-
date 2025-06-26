#!/bin/bash
cat <<EOF > /etc/odoo/odoo.conf
[options]
admin_passwd = ${ADMIN_PASSWORD:-odoo_18}
xmlrpc_port = 8069
addons_path = /mnt/extra-addons

db_host = ${DB_HOST}
db_port = ${DB_PORT}
db_user = ${DB_USER}
db_password = ${DB_PASSWORD}

limit_time_cpu = 999999999
limit_time_real = 999999999
session_store = db
EOF

exec odoo -c /etc/odoo/odoo.conf "$@"
