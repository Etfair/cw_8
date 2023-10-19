python3 -m venv venv
source venv/Scripts/activate.bat
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic --no-input
deactivate
#docker-compose up --build -d
#docker-compose exec app python manage.py migrate
