# BASIC CODE

# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nisp78@localhost:5432/todoapp'
# db = SQLAlchemy(app)
#
# migrate = Migrate(app, db)
#
# class Todo(db.Model):
#   __tablename__ = 'todos'
#   id = db.Column(db.Integer, primary_key=True)
#   description = db.Column(db.String(), nullable=False)
#   completed = db.Column(db.Boolean, nullable=False, default=False)
#
#   def __repr__(self):
#     return f'<Todo {self.id} {self.description}>'
#
# # db.create_all()
#
# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#   description = request.get_json()['description']
#   todo = Todo(description=description)
#   db.session.add(todo)
#   db.session.commit()
#   return jsonify({
#     'description': todo.description
#   })
#
#
# @app.route('/')
# def index():
#   return render_template('index.html', data=Todo.query.all())

# Here's the commands to give in the terminal after creating the database with createdb todoapp and activating it in postgres with psql todoapp
# todoapp=# \dt
# List of relations
# Schema | Name  | Type  | Owner
# --------+-------+-------+--------
# public | todos | table | nisp78
# (1 row)
#
# todoapp=# \d todos
# Table "public.todos"
# Column    |       Type        | Collation | Nullable |              Default
# -------------+-------------------+-----------+----------+-----------------------------------
# id          | integer           |           | not null | nextval('todos_id_seq'::regclass)
# description | character varying |           | not null |
# Indexes:
# "todos_pkey" PRIMARY KEY, btree (id)
#
# todoapp=# INSERT INTO todos (description) VALUES ('Do a thing 1');
# INSERT 0 1
# todoapp=# INSERT INTO todos (description) VALUES ('Do a thing 2');
# INSERT 0 1
# todoapp=# INSERT INTO todos (description) VALUES ('Do a thing 3');
# INSERT 0 1
# todoapp=# INSERT INTO todos (description) VALUES ('Do a thing 4');
# INSERT 0 1
# todoapp=# select * from todos;
# id | description
# ----+--------------
# 1 | Do a thing 1
# 2 | Do a thing 2
# 3 | Do a thing 3
# 4 | Do a thing 4
# (4 rows)

# terminal commands to launch the localhost and check the webapplication
# $ FLASK_APP=app.py FLASK_DEBUG=true flask run
# $ psql todoapp
# >>> select * from todos;

# # Takeaways
# Commits can succeed or fail. On fail, we want to rollback the session to
# avoid potential implicit commits done by the database on closing a connection.
# Good practice is to close connections at the end of every session used in a
# controller, to return the connection back to the connection pool.
# Pattern (try-except-finally)
#  import sys
#
#  try:
#    todo = Todo(description=description)
#    db.session.add(todo)
#    db.session.commit()
#  except:
#    db.session.rollback()
#    error=True
#    print(sys.exc_info())
#  finally:
#    db.session.close()

# example:

# # Here we import the flask class from the Flask module as well as the render method render_template
# from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
# # Here we import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# import sys
#
# # Here we create the application 'app'
# app = Flask(__name__)
# # Here we configure our Flask application to connect to a specific database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nisp78@localhost:5432/todoapp'
# # db variable/object that links SQLAlchemy to our flask app
# db = SQLAlchemy(app)
#
# # Here we define migrate which should equal an instance of the migrate class
# # linking to our Flask app and our SQLAlchemy database
# migrate=Migrate(app, db)
#
# # Here we create a child class and import the parent class db.Model
# class Todo(db.Model):
#     __tablename__='todos'
#     # id column (in SQL) or attribute (in Python)
#     id = db.Column(db.Integer, primary_key=True)
#     # description column (in SQL) or attribute (in Python)
#     description = db.Column(db.String(), nullable=False)
#
#     # Debugging statement
#     def __repr__(self):
#         return f'<Todo {self.id} {self.description}>'
#
# # Here we define a route that listens to the URL http://127.0.0.1:5000/todos/create posted by the user and in particular
# # listens to request that come in with a method post.
#
# @app.route('/todos/create', methods=['POST'])
# def create_todo():
#   error = False
#   body = {}
#   try:
#     description = request.form.get_json()['description']
#     todo = Todo(description=description)
#     db.session.add(todo)
#     db.session.commit()
#     body['description'] = todo.description
#   except:
#     error = True
#     db.session.rollback()
#     print(sys.exc_info())
#   finally:
#     db.session.close()
#   if error:
#     abort (400)
#   else:
#     return jsonify(body)
#
# # Here we set-up a route that listens to our homepage, when the user inserts the URL into the browser
# # include data that comes from the database
# @app.route('/')
# # here we define the route handler which will return a template HTML file and include data that comes from our database
# def index():
#     return render_template('index.html', data=Todo.query.all())

# MIGRATIONS - COMMANDS

# flask db init = Create initial migrations directory structures
# flask db migrate = Detects the model changes to be made, and creates a migration
# file with upgrade and downgrade logic set up

# TO APPLY MIGRATIONS WE NEED TO DROP THE EXISTING DATABASE FIRST AND RECREATE IT
# THEN RUN THE MIGRATIONS. COMMANDS:

# imac-di-nicola:todoapp nisp78$ dropdb todoapp
# imac-di-nicola:todoapp nisp78$ createdb todoapp
#
# imac-di-nicola:todoapp nisp78$ flask db migrate

# # imac-di-nicola:todoapp nisp78$ flask db upgrade (to upgrade the database)

# # imac-di-nicola:todoapp nisp78$ flask db downupgrade (to downgrade it)

# THE STEPS ARE:

# 1) WE CREATE A NEW COLUMN (FOR EXAMPLE: completed = db.Column(db.Boolean, nullable=False, default=False)
# 2) flask db init (to set-up folders to store migrations as versions of the database)
# 3) flask db migrate (to create tables for SQLALchemy models)
# 4) We make changes to the SQLAlchemy model, by, f.e., adding a column as in:
# completed = db.Column(db.Boolean, nullable=False, default=False)
# 5) flask db migrate (to generate a migration script based on the changes made)
# 6) We inspect the migration script in the folder versions
# 7) we alter it, such as:
# def upgrade():
    #     # ### commands auto generated by Alembic - please adjust! ###
    #     op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    #     # ### end Alembic commands ###

    # We also add:

    # op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')

    # op.alter_column('todos', 'completed', nullable=False)
    # # ### end Alembic commands ##
# 4) flask db upgrade
# 5) we can rollback this migration with flask db downgrade

# def upgrade():
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
#     # ### end Alembic commands ###

# BASICALLY BY DOING THIS WE CAN UPDATE THE DATABASE VIA THE FILE.PY IN THE versions
# FOLDER INSTEAD OF USING SQL COMMANDS FROM THE TERMINAL

# WE CHECK THE DATABASE WE psql todoapp and SELECT * FROM todos;

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nisp78@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False)

  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# note: more conventionally, we would write a
# POST endpoint to /todos for the create endpoint:
# @app.route('/todos', method=['POST'])
@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description, completed=False)
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['completed'] = todo.completed
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
  try:
    completed = request.get_json()['completed']
    print('completed', completed)
    todo = Todo.query.get(todo_id)
    todo.completed = completed
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({ 'success': True })


@app.route('/')
def index():
  return render_template('index.html', todos=Todo.query.order_by('id').all())
