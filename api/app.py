from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello world!'

@app.route('/fruits')
def fruits():
    beers = [
        {
            'brand': 'Guinness',
            'type': 'stout'
        },
        {
            'brand': 'Hop House 13',
            'type': 'lager'
        }
    ]
    list_of_fruits = ['banana', 'orange', 'apple']
    list_of_drinks = ['coke', 'milk', beers]
    return jsonify(Fruits=list_of_fruits, Drinks=list_of_drinks)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')