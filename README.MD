# Obey the Testing Goat

I use this repository to ster the code that I created reading the Harry's TDD book. The book is available online.
[Obey the Testing Goat](http://www.obeythetestinggoat.com/)

Good for:

 * Learning TDD
 * Learnin Python
 * Learning Django

I used Docker to create my environment.

##Setup Docker Eviroments:
### Steps
* prep: install docker compose

#### Part I: Selenium
* create a folder on docker VM / host machine (e.g. /Users/hongmeiqiu/docker/selenium_goat)
* go to /selenium_goat directory
* create the following files:
	* Dockerfile

			FROM python:3.4
			ENV PYTHONUNBUFFERED 1
			RUN mkdir /code
			WORKDIR /code
			ADD requirements.txt /code/
			# install firefox for debian "iceweasel"
			RUN apt-get update && apt-get install -y iceweasel
			RUN pip install -r requirements.txt
			ADD . /code/


	* requirements.txt

			Django
			selenium
			python-wd-parallel

	* docker-compose.yml

			selhub:  
			  image: selenium/hub
			  ports:
			    - 4444:4444

			nodeff:  
			  image: selenium/node-firefox-debug
			  ports:
			    - 5900
			  links:
			    - selhub:hub

			nodechrome:  
			  image: selenium/node-chrome-debug
			  ports:
			    - 5900
			  links:
			    - selhub:hub

			# selenium:
			#  build: .
			#  command: /bin/bash
			#  volumes:
			#    - .:/code

* build the docker image:
	* docker build -t selenium_goat:1.0 . 
* spin up the selenium hub:
	* docker-compose up
* to verify your selenium hub:
	* look up "selenium/node-firefox-debug" port number (e.g. 32769)
		* docker ps
	* look up docker's ip address (e.g. 192.168.59.103)
		* e.g. open up a new terminal on host machine, run command line: boot2docker ip
	* open up vnc via "Screen Sharing" app, type in host:port (e.g.: 192.168.59.103:32769)
	* Password is "secret".

#### Part II: Django
* follow [Obey the Testing Goat](http://www.obeythetestinggoat.com/) book online
	* on VM / host machine create a folder for goat tests (e.g. /Users/hongmeiqiu/docker/django_goat)
	* go to /django_goat directory
	* create functional_test.py

			from selenium import webdriver
			
			# browser = webdriver.Firefox() # original goat example code

			# note: replace the url with your docker's ip address + your selenium hub's docker port number (can be found via "docker ps")
			selenium_hub_url = 'http://192.168.59.103:4444/wd/hub'

			# open firefox browser on selenium hub
			browser = webdriver.Remote(
				command_executor=selenium_hub_url,
				desired_capabilities={"browserName": "firefox"})

			# note: replace the url with your docker's ip address + your django app's port number (can be found in )
			django_url = 'http://192.168.59.103:8000'

			# go to django app url (assume django app is up)
			browser.get(django_url)

			assert 'Django' in browser.title
	* execute the functional testing in docker:
		* docker run -it --rm -v /Users/hongmeiqiu/docker/django\_goat:/goat\_test selenium_goat:1.0 python /goat\_test/functional\_test.py
		* expect the test to fail, because there's no django instance running yet
	* create the following files:
		* Dockerfile

				FROM python:3.4
				ENV PYTHONUNBUFFERED 1
				RUN mkdir /goat
				WORKDIR /goat
				ADD requirements.txt /goat/
				RUN pip install -r requirements.txt
				ADD . /goat/		

		* requirements.txt

				Django
				psycopg2
		
		* docker-compose.yml

				db:
				  image: postgres
				web:
				  build: .
				  command: python manage.py runserver 0.0.0.0:8000
				  volumes:
				    - .:/goat
				  ports:
				    - "8000:8000"							    - "8081:8081"
				  links:
				    - db
		
	* spin off the django instance in docker:
		* docker-compose run web django-admin.py startproject superlists .
		* docker-compose up
	* execute the functional testing again:
		* shell in in the Django docker container:
			* 	docker exec -it django_web_1 bash
		* have the "Screen Sharing" open and run the test 
			*  python functional_test.py 
		* this time the test should work, check the "Screen Sharing"

##Stat the book

* I have two terminals open every time:
	*  one to execute the test on my Django docker image 
			
			docker exec -it djangoweb1 bash
			
	*  one to manage the git repository (I also used SourceTree)
* I tag the end of each chapter (suggested by the book) in my repository
* Skimming and scanning chapter 8-9


