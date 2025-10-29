from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"


with app.app_context():
    db.create_all()


# home page and post is give data and get is get it back to system
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")

            return f"ERROR: {e}"
    else:
        # gets all the info taht is created nad orders it on how it is made
        tasks = MyTask.query.order_by(MyTask.created).all()
        # thsi gives teh info in tasks to inde.html
        return render_template("index.html", tasks=tasks)

# hhhhs


# Delete

@app.route("/delete/<int:id>")
def delete(id: int):
    # get the info in my task like id content
    delete_task = MyTask.query.get_or_404(id)
    try:
        # we are taking the info that is gotten in delete task helps it arrange well
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"Error deleting task: {e}"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def edit(id: int):
    # get the info in my task like id content
    # this is basically kinda like the connecting point as this is mentioned in html as this get the info and then arranged into like a Mytask order
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        # THIS BASICALLY ADDS THE NEW THING ADDDED INTO THE TASK.COntent in the thing
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:  # thsi basically puts the exception taht happened makes us able to see taht as an error on top of teh page
            return f"Error:{e}"
    else:
        return render_template('edit.html', task=task)


# flask is a manager for all the routes
if __name__ == "__main__":  # prevents error if we import
    app.run(debug=True)


# how to activate env is by .\env\Scripts\Activate.ps1
# <!DOCTYPE html>
# <html lang="en">
    # <head>
    # <meta charset="UTF-8" />
    # <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    # <meta name="viewport" content="width=device-width, intial-scales=1.0" />
    # <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}" />
    # {% block head%}{% endblock %}
    # </head>
    # <body>
    # {%block head%} {%endblock%}
    # </body>
# </html>
