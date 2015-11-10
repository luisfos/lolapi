import os
import pymongo
from flask import Flask, render_template
import static.pyscripts.Main as link
#run this program in pycharm for localhost
app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
#client = pymongo.MongoClient(os.environ['OPENSHIFT_MONGODB_DB_URL'])

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/<champName>')
def champion(champName):
	# return link.ctrl.builds
    return "banter"

if __name__ == "__main__":
    app.run()

