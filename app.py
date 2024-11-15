from flask import Flask
from flask_restful import Api
from models import db
from resources import DepartmentResource, CourseResource, UserResource, AttendanceLogResource, StudentResource  # Import other resources similarly

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendancemanagementsystem.db'  # Use any database URI of your choice
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

# Register resources
api.add_resource(DepartmentResource, '/departments', '/departments/<int:department_id>')
api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>')
api.add_resource(StudentResource, '/students', '/students/<int:student_id>')
api.add_resource(AttendanceLogResource, '/attendance_logs', '/attendance_logs/<int:log_id>')
api.add_resource(UserResource, '/users', '/users/<int:user_id>')
# Register other resources similarly

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the database tables
    app.run(debug=True)