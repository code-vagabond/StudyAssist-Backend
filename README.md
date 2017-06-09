# StudyAssist Backend #

StudyAssist Backend ist based on the Flask-Admin module and provides the application with basic admin functionalities. The examination office can login as admin to modify and publish module information. Student can use the HRZ-Account to login and track their progress.

Later on function to fetch module informations will be implemented. 

The Backend uses SQLAlchemy as a data abstraction.


# Using the crawler to fetch data
StudyAssist fetch data based on student credentials and populate a Postgres Database. First create the postgres database and input the config into crawler/database.ini then run crawler.py to populate this database.


# Install and run:

1. Clone the repository::

```sh
git clone https://github.com/code-vagabond/StudyAssist-Backend.git
cd StudyAssist-Backend.git
```

2. Create and activate a virtual environment::

```sh
virtualenv env
source env/bin/activate
```

3. Install requirements::
```sh
pip install -r 'requirements.txt'
```

4. Run the application::
```sh
python app.py
```


```sh
if not os.path.exists(database_path):
 build_sample_db()
```
