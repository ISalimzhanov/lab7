from flask import Flask
import flask

app = Flask(__name__)

fizmat_cnt = 0
ktl_cnt = 0


@app.route('/', methods=['GET'])
def home_page():
    return flask.render_template('index.html', fizmat_cnt=fizmat_cnt, ktl_cnt=ktl_cnt)


@app.route('/fizmat', methods=['GET'])
def fizmat_page():
    return flask.render_template('fizmat.html')


@app.route('/ktl', methods=['GET'])
def ktl_page():
    return flask.render_template('ktl.html')


if __name__ == '__main__':
    app.run()
