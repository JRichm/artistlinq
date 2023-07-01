""" ### Server Imports ### """

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'dev'

""" ### Flask Routes ### """

  ### " View Homepage " ###
@app.route('/')
def index():
    return render_template('index.html')
  

""" ### Server Methods ### """

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)