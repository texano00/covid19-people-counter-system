from flask import Flask, render_template, jsonify
from db import getCountByCode

app = Flask(__name__)

@app.route('/people/<code>')
def getPeopleByCode(code):
    return jsonify(getCountByCode(code))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')