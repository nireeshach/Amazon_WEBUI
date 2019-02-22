# Amazon_WEBUI

Amazon_WebUI
Amazon_WebUI application which takes product url from the user and shows High Quality Reviews and Low Quality Reviews along with Adjusted star Rating and Amazn Original Rating and their difference.

Setup
You need to follow the below steps to setup the UI

Install "Python 3.6.x"

You can use “virtualenv” for Python if you want to have separate environment for each project so that it won’t effect other projects and this recommended.

Create python virtualenv in .venv directory in the cloned directory. You can use the below command to create virtualenv, if python3.6-venv and pip are installed.

 1.python -m venv ".venv"
 2. source .venv/bin/activate (to activate the virtualenv)
 
 
Install dependencies given in "requirements.txt" file. You can use the command below to install all the dependencies in one shot. * pip install -r requirements.txt

We are using "gunicorn" as web server to bringup the web UI. Gunicorn is a Python Web Server Gateway Interface (WSGI) HTTP server. You can run the command below to access the UI from the browser, using localhost or system ip and the port mentioned in command.

 		i. gunicorn -b 0.0.0.0:port main:app --timeout 360
 	       Example: gunicorn -b 0.0.0.0:5000 main:app --timeout 360
 	      By running the command above, you should be able to access the UI from "localhost:5000" or "machine-ip:5000"
        
        
You can also run gunicorn instance as daemon, by running the command below gunicorn -b 0.0.0.0:port main:app --workers=1 --timeout 360 --daemon

Note: You need to run the above command from the same directory of "main.py" file.

© 2019 
