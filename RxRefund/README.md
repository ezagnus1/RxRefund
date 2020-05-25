# rxrefund-dashboard 2019


# Database settings
Change database settings  /rxdashboard/dashboard/settings.py
Line 78  with your own database setting . Check your port number,database name,
and password.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'RXREFUND',
        'USER': 'postgres',
        'PASSWORD': '123456',
        'HOST': '',
        'PORT': '5433'
    }
}
```


# Postgre library path
Add-change tha path with your Postgre path in /rxdashboard/dashboard/models.py
line 7.


```python
os.environ['DYLD_LIBRARY_PATH'] = '/Library/PostgreSQL/12/lib'
```

# Before your first run:
Make sure you have a database 'RXREFUND' . Don't create
the tables. Django creates it after migrations.

# Migrations
Open your terminal or pycharm terminal ;
First step;

```bash
$ python manage.py migrate
```
Then;

```bash
$ python manage.py makemigrations
```

# How to run
If you are using pycharm first ckeck your configuration setting of project.
Make sure that it is Django server.
You can run the code with run botton or from pycharm terminal;

```bash
$ pyhton manage.py runserver
```


Go to output server:

```bash
Starting development server at http://127.0.0.1:8000/
```
