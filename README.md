# StudyAssist Backend #

StudyAssist Backend ist based on the Flask-Admin module and provides the application with basic admin functionalities. The examination office can login as admin to modify and publish module information. Student can use the HRZ-Account to login and track their progress.

Later on function to fetch module informations will be implemented. 

The Backend uses SQLAlchemy as a data abstraction.

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

The first time you run this example, a sample sqlite database gets populated automatically. To suppress this behaviour,
comment the following lines in app.py:::
```sh
if not os.path.exists(database_path):
 build_sample_db()
```
