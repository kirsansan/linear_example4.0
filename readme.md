<h2>Task</h2>

- You need to determine your own movements in the ETHUSDT futures price, 
excluding from them movements caused by the influence of the BTCUSDT price. 
Describe what methodology you chose, what parameters you selected, 
and why (the rationale can be documented in the README).
- Write a Python program that monitors the ETHUSDT futures price in real time 
(with minimal delay) and, using the method you choose, determines your own ETH price movements. 
If the price changes by 1% in the last 60 minutes, the program displays a message in the console.
In this case, the program should continue to work, constantly reading the current price.


<h3>Explanation</h3>
Please find the explanation of first part of task in file explanation.pdf

<h3>How to prepare.</h3>
this project use next components:
- python as a base platform (3.10 and 3.11 are supported)
- SQLAlchemy as ORM
- PostgreSQL for saving temporary data (available mode of work without using database)
- FastAPI for getting few option for interface creation and interact with user


<h3>How to install.</h3>
- clone project to own disk in new directory
- activate virtual environment (python -m venv venv)
- install all needs packages (pip install -r requirements.txt)
- see next step for configure

<h3>How to configure.</h3>
Please pay your attention to configure .env file.
You can find example in root of your project directory (.env.example)
please fill all parameters with your data and save the changed file as .env

in current version of app we use ByBit API.
you have to take key's for working with ByBit API.
API_KEY 
SECRET_KEY 


After that you need create empty database.
don't see this if you want to use app without database (on-line mode)
you may use command
>psql -U postgres;
>CREATE DATABASE <database_name>

or 
> createdb -U postgres <database_name>

alternatively you can use pgadmin or other interface app.

Use next commands for tables creation
>alembic upgrade head


Netx step - check parameters in file config.config
for you interest look for 
>ALARM_THRESHOLD = 0.01  # 0.01 = one percent 
> 
>BAD_CORRELATION_THRESHOLD = 0.72  # see explanation in research.py
> 
>TIME_THRESHOLD = 3600  # 3600  # default 60*60 seconds = 1 hour
> 
>VERBOSE_MODE = True  # to print or not to print - that is the question
> 
>REBUILD_MODELS_TIME = 60  # seconds. default = 60*60; if you don't want rebuilding - set 0


make sense set VERBOSE_MODE in True for debugging 

<h3>Ноw it works.</h3>

Start the server with
>python research.py

this will give you an idea of how the parameters are calculated

So. Are you ready for a start? start the app with next commands 
>uvicorn src.main:app 

optional use --host and --port option



you will find API documentation (smile here) how to use endpoints   
http://127.0.0.1:8000/docs/ or 
http://127.0.0.1:8000/redoc/
use it with any browser what you like

Main enpoints for use are: 
http://127.0.0.1:8000/status - for status display;
http://127.0.0.1:8000/check - command for checking; 
http://127.0.0.1:8000/rebuild - command for rebuild math models;




<h3>Testing</h3>

To run the tests, ensure that you have pytest installed in your virtual environment. 
If you don't have it, you can install it using: pip install pytest. 
Next, navigate to the root directory of your project and execute: pytest


<h3>Docker</h3>

For create docker image use:
build docker image
>docker build -t "NAME" .

for run container execute (pay attention now it works on port 8000):
>docker run "NAME"



Have a nice day! See you!
with best wishes, <h5>kirill.s</h5>
