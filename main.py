from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(12), unique = True, nullable = False)
    # image = db.column(db.Bytes, unique = True, nullable = False)
    ticket = db.column(db.String(250))

    # code - database, After scanning through db, will assign code based on ticket ocr data
    # will look for engineers in the db - will allocate the engineer free or look for engineer timeline
    # client gui will also contain a button - ticket/problem status
    # Once the client clicks on the client button, it will show ticket resolved and patch it to db


    def __repr__(self):
        print(f"{self.customer_id}\n{self.ticket}")

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return "Index"

@app.route("/users")
def get_users():
    users = Users.query.all()
    output = []
    for user in users:
        output.append({"Customer ID": user.customer_id, "Ticket": user.ticket})

    return {"users-data":output}

@app.route("/users/<cid>")
def get_user(cid):
    customer_id = cid
    user = Users.query.get_or_404(customer_id)
    return {{"Customer ID": user.customer_id, "Ticket": user.ticket}}

@app.route("/users/", methods = ["POST"])
def post_drink():
    user = Users(customer_id = request.json["Customer ID"], ticket = request.json["image"])
    db.session.add(user)
    db.session.commit()
    return "User Request successfully created! Your ticket will be resolved soon"

@app.route("/users/<cid>", methods = ["DELETE"])
def delete_user(cid):
    customer_id = cid
    user = Users.query.get(customer_id)
    if user is None:
        return {"Deletion Status": "No such user found in the record"}
    db.session.delete(user)
    db.session.commit()
    return {"Deletion Status": "User successfully deleted from the record"}

if __name__ == "__main__":
    app.run(debug=True)
