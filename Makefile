# USE TABS ONLY! NO SPACES! Because "make" util wants this!

all:
	pip install -r requirements.txt
	./manage.py runserver

