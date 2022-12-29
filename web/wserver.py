from flask import Flask

app = Flask(__name__)

@app.route('/')
def homepage():
    return "<h1>Google Drive Clone Bot by <a href='https://github.com/culturecloud'>Culture Cloud</a></h1>"

if __name__ == "__main__":
    app.run()

