from flask import Flask
from flask import request
app = Flask(__name__)


# @app.route('/home')
# def hello_world():  # put application's code here
#     return 'Hello World!'
@app.route('/home')
def home():
    return 'Welcome to the homepage!'
# @app.route('/about')
# def about():
#     return 'This is the about page.'
@app.route('/user/<username>')
def show_user_profile(username):
    return f'<h1>My Profile username: {username}!</h1>'

@app.route('/hello/<name>')   #  Добавление нового маршрута с параметром:
def hello(name):
    return f'Hello, {name}!'

@app.route('/double/<int:number>')   #  Использование преобразователя int
def double_number(number):           # app.route('/square/<int:number>', methods=['POST']) можно менять метод
    return f'{number} doubled is {number * 2}'

@app.route('/test_endpoint_with_bady_param/', methods=['POST'])
def square2(number):
    data = request.form.get('data')
    print(data)
    return f'This is ...{data}'

@app.route('/reverse/<path:text>')   #  Использование преобразователя path:
def reverse_text(text):
    return f'{text} reversed is {text[::-1]}'


@app.route('/profile_uuid/<uuid:user_uuid>')
def get_profile_uuid(user_uuid):  # put application's code here
    return f'<h1>My Profile user_uuid: {user_uuid}!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
