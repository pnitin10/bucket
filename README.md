# Bucket
Bucket is a website that helps track of daily tasks.

This project is broken up into a backend and frontend. 
The backend contains the Django project which uses the Django Rest Framework to host a simple API.
The frontend uses React and queries data from the API.

Run the following commands to get started:

Backend
-------
Technologies Used
-----------------
1. Python 3.6.10
2. Django
3. Django REST Framework
4. virtualenv

Installation
------------
Clone the repo git clone https://github.com/pnitin10/bucket.git/ and navigate to the project directory

Create and activate a virtual environment<br />
e.g <br />
Creation - virtualenv -p python3.6 env<br />
Activate - source/bin/activate<br />
Deactivate - decativate<br />
Install dependencies pip install -r requirements.txt<br />

From the project root directory, run the app

Set up the database
-------------------
<ul>
  <li>Create a mysql database using any other possible methods.</li>
  <li>Navigate to bucket/backend/src/bucket/settings.py file, then update the database settings to hold your database name, your mysql user, password and any other neccessary information</li>
  <li>Make migrations.</li>
  <li>Run cd bucket/backend/src/ and python manage.py makemigrations to create the models for the app.</li>
  <li>After making migrations, run python manage.py migrate to create necessary tables in the database.</li>
  <li>Run cd bucket/backend/src/ and python manage.py runserver to get the app running</li>
</ul>


Frontend
--------
Technologies Used
-----------------
React.js 16

Installation
------------
1. npm i or npm install
2. npm start


