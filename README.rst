## StudyAssist Backend ##

StudyAssist Backend ist based on the Flask-Admin module and provides the application with a module database. The examination office can login to modify and publish module information. Student can use the HRZ-Account to login and track their progress.

Later on function to fetch module informations will be implemented. 

The Backend uses SQLAlchemy as a data abstraction.

To run this example:

1. Clone the repository::

     git clone https://github.com/code-vagabond/StudyAssist-Backend.git
     cd flask-admin

2. Create and activate a virtual environment::

     virtualenv env
     source env/bin/activate

3. Install requirements::

     pip install -r 'examples/auth/requirements.txt'

4. Run the application::

     python app.py

The first time you run this example, a sample sqlite database gets populated automatically. To suppress this behaviour,
comment the following lines in app.py:::

     if not os.path.exists(database_path):
         build_sample_db()
