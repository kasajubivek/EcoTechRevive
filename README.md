Installation Prerequisites
Python 3.8+
Django 5.0.6
Git

Steps

Clone the repository:
git clone https://github.com/VatsalPatel19/EcoTechRevive.git
cd EcoTechRevive

Create a virtual environment:
python -m venv env

Activate the virtual environment:

On Windows:
.\env\Scripts\activate

On macOS/Linux:
source env/bin/activate

Install the required packages:
pip install -r requirements.txt

Apply database migrations:
python manage.py makemigrations
python manage.py migrate

Create a superuser (admin):
python manage.py createsuperuser

Run the development server:
python manage.py runserver
Open your browser and go to http://127.0.0.1:8000/



