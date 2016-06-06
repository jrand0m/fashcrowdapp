# USE TABS ONLY! NO SPACES! Because "make" util wants this!

init:
	pip install -r requirements/dev.txt
	./manage.py migrate

superuser:
	./manage.py createsuperuser --email admin@flashcrowd.app

all:
	pip install -r requirements/dev.txt
	./manage.py migrate
	./manage.py runserver 0.0.0.0:8000

run: | all

test:
	echo "No tests for now :<"
