from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json
import os
import uuid
app = Flask(__name__)
app.secret_key = os.urandom(24) 


# Route to serve the HTML page
@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4()) 
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
    print(story)


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
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4()) 

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
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4()) 
    print(session['user_id'])
    return render_template('enterAddress.html')


@app.route('/writeStory')
def writeStory():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4()) 
    return render_template('writeStory.html')


@app.route('/submitStory', methods=['POST'])
def submitStory():
    data = request.data  # Get the raw string of JSON data sent from the client
    data_body = json.loads(data)
    data_str = data_body.get("data")
    write_to_story_json(json.loads(data_str))
    write_to_door_json(json.loads(data_str))
    write_to_tunnel_json(json.loads(data_str))
    return 'story has been saved'




def write_to_story_json(data_dict):
    newStory = {
        "title": data_dict.get("nameOfDoor"),
        "story": data_dict.get("story"),
        "name": data_dict.get("byWho"),
        "location": data_dict.get("address"),
        "google_map": data_dict.get("google_map"),
    }

    print(newStory)

    with open("story_data.json", 'r+') as f:
        existing_data = json.load(f)
        print(type(existing_data))
        existing_data[session['user_id']] = newStory
        f.seek(0)
        json.dump(existing_data, f, indent=4)



def write_to_door_json(data_dict):
    newDoor = {
        "name": data_dict.get("nameOfDoor"),
        "doorImage": "door23.png",
        "userId": session['user_id']
    }
    with open("doors_data.json", 'r+') as f:
        existing_data = json.load(f)
        existing_data[session['user_id']] = newDoor
        f.seek(0)
        json.dump(existing_data, f, indent=4)


def write_to_tunnel_json(data_dict):
    newTunnel = {
        "story": data_dict.get("story"),
        "id": session['user_id'],
        "StoryImage":"story13.png"
    }
    with open("tunnel_data.json", 'r+') as f:
        existing_data = json.load(f)
        existing_data[session['user_id']] = newTunnel
        f.seek(0)
        json.dump(existing_data, f, indent=4)



if __name__ == '__main__':
    app.run(debug=True)