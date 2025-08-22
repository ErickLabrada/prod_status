from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import time
import json
import os

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

DATA_FILE = 'data.json'

def load_start_time():
    if not os.path.exists(DATA_FILE):
        return save_start_time(time.time())
    with open(DATA_FILE, 'r') as f:
        return json.load(f).get('start_time', time.time())

def save_start_time(start_time):
    with open(DATA_FILE, 'w') as f:
        json.dump({'start_time': start_time}, f)
    return start_time

@app.route('/')
def index():
    if not os.path.exists(DATA_FILE):
        save_start_time(time.time())  # Creates initial file
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    start_time = data.get('start_time', time.time())
    guilty = data.get('guilty', 'Desconocido')  # Fallback name
    return render_template('index.html', start_time=start_time, guilty=guilty)


@app.route('/reset')
def reset():
    new_time = time.time()
    save_start_time(new_time)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
