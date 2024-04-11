from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
app = Flask(__name__)

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# API route to provide JSON data
@app.route('/data')
def data():
    f = open('doors_data.json')
    doors = json.load(f)
    f.close()
    return doors


@app.route('/story/<user_id>')
def story(user_id):
    f = open('story_data.json')
    storys = json.load(f)
    f.close()

    story = storys[user_id]


    return render_template('story.html', story=story)


@app.route('/tunnel/<user_id>')
def tunnel(user_id):
    f = open('tunnel_data.json')
    tunnel = json.load(f)
    f.close()

    tunnel = tunnel[user_id]
    return render_template('tunnel.html', tunnel=tunnel)


@app.route('/createDoor')
def form():
    doorFrame_folder = os.path.join('static', 'imga', 'doorFrame')
    doorFrame_files = [f for f in os.listdir(doorFrame_folder) if f.endswith('.png')]

    doorInner_folder = os.path.join('static', 'imga', 'doorInner')
    doorInner_files = [f for f in os.listdir(doorInner_folder) if f.endswith('.png')]



    return render_template('createDoor.html', doorFrame_files=doorFrame_files, doorInner_files=doorInner_files)



@app.route('/submitNewDoor', methods=['POST'])
def submit():
    name = request.form['name']
    doorImage = request.form['doorImage']
    userId = request.form['userId']

    # Prepare data as a dictionary
    data = {'name': name, 'doorImage': doorImage, 'userId': userId}    
    # Save or append data to a JSON file
    append_data(data)
    return 'Form submitted! Data has been saved.'


def append_data(data, filename='doors_data.json'):
    try:
        with open(filename, 'r+') as f:
            existing_data = json.load(f)
            existing_data["doors"].append(data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)
    except FileNotFoundError:
        with open(filename, 'w') as f:
            door_json = { "doors": data}
            json.dump([door_json], f, indent=4)




@app.route('/address')
def address():
    return render_template('enterAddress.html')




if __name__ == '__main__':
    app.run(debug=True)