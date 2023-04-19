import uuid
from flask import Flask, redirect, jsonify, url_for, request, abort
# import json

# initialisiere Flask-Server
app = Flask(__name__)

# create unique id for lists, entries
# todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
# todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
# todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
# todo_1_id = uuid.uuid4()
# todo_2_id = uuid.uuid4()
# todo_3_id = uuid.uuid4()
# todo_4_id = uuid.uuid4()

# define internal data structures with example data
toDoLists = [
    # {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    # {'id': todo_list_2_id, 'name': 'Arbeit'},
    # {'id': todo_list_3_id, 'name': 'Privat'},
    {'id', 'name'}
]
toDoListEntries = [
    # {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    # {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    # {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    # {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
    {'id','name','description','list'}
]

# definiere Route für Hauptseite
@app.route('/todo-list', methods = ["GET","POST"])
def handleToDoLists():
    if request.method() == 'GET':
        return jsonify(toDoLists)
    elif request.method() == 'POST':
        newList = request.get_json(force=True)
        # print('Got new list to be added: {}'.format(newList))s
        # create id for new list, save it and return the list with id
        newList['id'] = uuid.uuid4()
        toDoLists.append(newList)
        return jsonify(newList), 200

@app.route('/todo-list/{listID}', methods = ["GET","DELETE","PATCH"])
def handleToDoList(listID):
    i, listItem = checkListID(listID)
    match request.method(listID):
        case 'GET':
            return jsonify([i for i in toDoListEntries if i['list'] == listID])
        case 'DELETE':
            toDoLists.remove(listItem)
            return 200
        case 'PATCH':
            newName = request.get_json(force=True)
            i[listID] = newName
            return 200 

def checkListID(listID):
    for i in toDoListEntries:
        if i['id'] == listID :
            listItem = i
            break

    if not listItem:
        abort(404)
    return i,listItem           

@app.route('/todo-list/{list_id}/entry', methods = ["POST"])
def insertNewEntry(listID):
    i, listItem = checkListID(listID)
    newEntry = request.get_json(force=True)
    newEntry['id'] = uuid.uuid4()
    newEntry.append(newEntry)
    return jsonify(newEntry), 200


    

@app.route('/entry/{entry_id}', methods = ["PATCH","DELETE"])
def handleEntry():
    
    if request.method == 'PATCH':
        print('')

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
   app.run(debug = True)
   app.run(host='0.0.0.0', port=5000)



