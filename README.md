# Rasa_flight_tickets
Mirafra's RASA Chatbot for booking flight tickets | flask backend

Steps to run:

rasa train

Working directory should contain the following :
1. Flask folder
2. Rasa folder
3. .dockerignore
4. .env
5. .gitignore


Flights chatbot

1. export FLASK_APP=Flask/app.py
  - flask run --port 5000
2. rasa run --cors "*" --enable-api --model Rasa/rasa_main/models --log-file Rasa/rasa_main/story_graph.dot --endpoints Rasa/rasa_main/endpoints.yml -p 5005
3. rasa run actions --actions Rasa/rasa_main -p 5055

or

1. python app.py
2. rasa run --cors "*" --enable-api
3. rasa run actions

Sample flight ticket requirements:
- name: Vishal
- contact number: 9898989898
- From: mumbai
- To: london
- departueDate: 2021-11-10
- returnDate: 2021-11-11 
- nonstop: false
- budget: 300000


Virtual environemnt: Without docker

action_endpoint:
 url: "http://localhost:5055/webhook"

Two requirements.txt files : 1 in Flask folder and 2nd in Rasa folder

Python : 3.7.0
rasa: 2.8.6
spacy: 3.1.3
rasa-sdk: 2.8.2
python-dotenv 0.19.0
rasa : pip: 21.1.3
rasa : setuptools 54.2.0
rasa : wheel : 0.36.2
flask : pip  21.2.4
flask : setuptools 57.4.0
flask : wheel 0.37.0



Docker:
Docker should be installed.
In endpoints.yml :
action_endpoint:
 url: "http://rasa_action_server:5055/webhook"

docker-compose build
docker-compose up --no-deps rasa_train
docker-compose --env-file .env up

I am storing the trained model with the name model_in_use
anyhow, the model recently trained in the list from models folder will be loaded for rasa run command, not necessariliy model_in_use model if u put the name of the old model as model_in_use. for rasa run only recently trained will be loaded irrespective of any name


To generate Authentication key:
1. Register/Sign-in for self-service API on amadeus : https://developers.amadeus.com/get-started/get-started-with-self-service-apis-335
2. Go in Self-Service MyWorkSpace option
3. Create new app
4. Go inside your app or icon and get the API KEY and API SECRET
This is the Authentication guide : https://developers.amadeus.com/self-service/apis-docs/guides/authorization-262

