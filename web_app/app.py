from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", title='Home Page')

@app.route("/data")
def data():
    return render_template("Data.html", title='Data Page')

@app.route("/data_presenation")
def data_presenation():
    return render_template("data_presentation.html", title='Data Presentation')


if __name__ == "__main__":
    app.run(debug=True)