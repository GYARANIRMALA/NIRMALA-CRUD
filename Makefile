env-setup:
	rm -rf venv
	# Python 3.9.5
	python3.8 -m venv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt

run-local:
	source venv/bin/activate; \
	export CONFIG_PATH=configs/local.cfg; \
	python manage.py makemigrations; \
	python manage.py migrate; \
	black .; \
	python manage.py runserver