## Backend:

```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
cd taskmgmt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Frontend

```bash
cd taskmgmt-frontend
python -m http.server 3000
```

http://localhost:3000/dashboard.html
