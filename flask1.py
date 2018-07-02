#!/usr/bin/python3

# import
from flask import Flask, render_template

app = Flask(__name__)

page='''<h1>Python is cool</h1>'''

#defining routes  -- /test is the url end to be typed
@app.route('/test')

# defining function on behalf of /test
def hello():
    return page

# route for another html page
@app.route('/adhoc')
# function on behalf of /adhoc
def webpage():
    url_for('static', filename='register.css')
    return render_template('adhoc.html')

# route for cmd
@app.route('/cmd')

def command():
    out = subprocess.getoutput('date')
    return out

if __name__ == '__main__':
    #   0.0...  for runnable on every machine
    app.run(host='0.0.0.0',port=80)
