from todolist import app
from todolist import db   
from todolist.models import Todo 

if __name__ == "__main__":
    db.create_all()    
    app.run(debug=True)

