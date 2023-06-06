# import Flask ?

from flask import Flask
from flask import request, redirect, url_for
from flask import  render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# ### create your first app
app = Flask(__name__)  ## __name__  ==> python assign this variable with module name

#### connect to database
# tell the application the database path you need

## http://www.ggogle.com/mm
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)  # you are now connected sqlite
# instance folder---> contain database --->

app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')


## customize page 404 not found
@app.errorhandler(404)
def page_not_found(error):  # you must pass the error object to the function
    return  f"<h1 style='color:red'> Sorry the request page not found on the server  </h1>";

#################### Model Section ##################
class Post(db.Model):
    __tablename__= 'Posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)




@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("Posts/home.html", posts=posts)








@app.route("/post/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        image = request.files["image"]
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        post = Post(title=title, body=body, image=filename)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("Posts/new_post.html")

@app.route("/post/<int:id>/edit", methods=["GET", "POST"])
def edit_post(id):
    post = Post.query.get(id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.body = request.form["body"]
        if request.files.get("image"):
            image = request.files["image"]
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            post.image = filename
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("Posts/edit_post.html", post=post)

@app.route("/post/<int:id>/delete")
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == '__main__':
    print(f" this is my module {__name__}")
    ### start flask app
    app.run(debug=True)