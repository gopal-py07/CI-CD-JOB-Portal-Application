
step 1. unzip the code the zip file

stpe 2. open terminal then navigate to (QuizApplication) dir and Aactivate the vertual envimenet ..(envquiz)
	
	navigate to

		cd envquiz/bin
	run cmd
		source activate
	or
	2.1. create new verual env using below command
		python3 -m venv (name of new vertual env)

	2.2 activate new vertual env

		navigate to

		cd (name of new vertual env)/bin
	run cmd
		source activate

	2.3. install all requriments using blow command
		
		navigate to the main project

			cd quizprj

		the run cmd
		
		pip3 install -r requriments.txt

	2.4 please skipp the 3rd step
		

step 3. naviagte to main project 

	cd quizprj

step 4. python3 manage.py runserver 

step 5. copy the from terminal then open browser pest url.

------------------------------------------------------------------
now dockerize the quiz application 

note: move to core project folder where dockerfile presents
	e,g quizprj
--------------------------------------------------------------
step 6. start your docker desktop or start docker using command 

	run cmd
		docker run

ste 7. By run below command the app will conatinerise and image are up and running.
	
	docker-compose -f docker-compose.yml up -d --build

step 8. check docker deskstop and images and conatiner are cretea up and runing
	
	or
	docker ps
	docker ps -a
	dokcer images


	
step 9 . open browser localhost:8000

step 10. push you image to docker hub
	
	dokcer push (image name)

ste 11. create a pod run below cmd

	kubectl apply -f deployment.yml

step 12. check pods

	kubectl get pods	

step 13. RUN ON KUBENRATE CLUSTER 8000 WITH NORDPORT

	kubectl expose deployment django-backend-quiz-app  --type=NodePort --port=8000

step 13. minikube services  run command

	minikube service --all

step 14. open url in browser

	




