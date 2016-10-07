run:
	(\
	source venv/bin/activate; \
	python main.py; \
	)

setup:
	virtualenv -p /usr/bin/python3.5 venv
	(\
	source venv/bin/activate; \
	pip install -r requirements.txt; \
	)
clean:
	rm -R __pycache__
	rm *.pyc
