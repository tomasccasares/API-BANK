## Description
  This project is about a banking API that allows users to register, deposit money into their accounts and transfer funds to other people.
  
## Features
- User registration: Users can create an account with the bank by providing the necessary information.
- Deposits: Users can make deposits of money into their accounts.
- Transfers: Users can transfer funds to other persons registered with the bank.
- Authentication: JWT is used to authenticate and authorize user requests.

## Technologies
- Python.
- Django.
- PostgreSQL.
- JWT (JSON Web Tokens).

## Installation
- Clone this repository: `git clone https://github.com/tomasccasares/-API-REST-DJANGO`.
- Go to the project directory: `cd cs_api`.
- Install dependencies: `pip install -r requirements.txt`.
- Configure the database in the `settings.py` inside the project's `cs_api` folder.
- Performs database migrations: `python manage.py makemigrations && python manage.py migrate`.
- Create a super user administrator: `python manage.py createsuperuser`.
- Start the local server: `python manage.py runserver`.
