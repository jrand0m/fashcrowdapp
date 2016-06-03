# USE TABS ONLY! NO SPACES! Because "make" util wants this!

superuser:
	./manage.py createsuperuser --email admin@flashcrowd.app

all:
	pip install -r requirements.txt
	./manage.py migrate
	./manage.py runserver
