import requests
from flask import Flask, render_template, request

def request_decorator(function):
    def wraper():
        global data
        data = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
        data = data.json()
        return function(data)
    return wraper

app = Flask(__name__)

@app.route('/', endpoint='home')
@request_decorator
def home(data=None):
    global blogs
    blogs = data
    return render_template('index.html', all_posts=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog/<int:index>')
def blog(index):
    requested_post = None
    for blog_post in data:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == '__main__':
    app.run(debug=True)
