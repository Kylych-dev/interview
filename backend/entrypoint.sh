#!/bin/bash


sleep 4

python3 manage.py migrate

python manage.py create_default_admin


python manage.py loaddata fixtures/sewingworkshop.json
python manage.py loaddata fixtures/warehouse.json
python manage.py loaddata fixtures/client.json
python manage.py loaddata fixtures/order.json
python manage.py loaddata fixtures/product_template.json
python manage.py loaddata fixtures/accounts.json
python manage.py loaddata fixtures/product.json
python manage.py loaddata fixtures/material_template.json

exec "$@"