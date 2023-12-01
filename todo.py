from flask import Flask , jsonify , request , abort
app = Flask(__name__)

tasks = [
    {
        'id':1,
        'title':'Mark your attendance.',
        'description':'Everyone has to mark their attendance.It is mandatory',
        'done': False
    },
    {
        'id':2,
        'title':'Write your #standup.',
        'description':'Everyone has to write their #standup daily.',
        'done':False
    }
]

@app.route('/todo' , methods=["GET"])
def display_todo():
    return jsonify(tasks)

@app.route('/todo',methods=["POST"])
def add_todo():
  if not request.json:
     abort(500)

  id = request.json.get('id',None)
  title = request.json.get('title',None)
  description = request.json.get('description','')

  if id is None or title is None:
     return jsonify(message="Invalid Request") , 500
  
  tasks.append({
     'id':id,
     'title':title,
     'description':description,
     'done':False
  })

  return jsonify(tasks)

@app.route('/todo/<int:id>', methods=["DELETE"])
def delete_todo(id):
   global tasks
   tasks = [task for task in tasks if task["id"] !=id]

   return jsonify(tasks)

def update(task,task_id,data):
   if task["id"] == task_id:
      if "title" in data:
         task["title"]=data["title"]
      if "description" in data:
         task["description"]=data["description"]

   return task

@app.route('/todo/<int:id>' , methods=["PUT"])
def update_todo(id):
   if not request.json:
      abort(500)

   id = request.json.get('id',None)
   title = request.json.get('title',None)
   description = request.json.get('description','')

   if id is None or title is None:
      return jsonify(message="Invalid Request") , 500
   
   global tasks
   tasks = [update(task,id,request.json) for task in tasks]

   return jsonify(tasks)