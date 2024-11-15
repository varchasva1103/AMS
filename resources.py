from flask_restful import Resource, reqparse
from models import db, Department, Course, Student, AttendanceLog, User

class DepartmentResource(Resource):
    def get(self, department_id=None):
        if department_id:
            # Get a specific department and its related courses
            department_data = db.session.query(
                Department
            ).filter(Department.id == department_id).first()

            if department_data:
                # Query all courses that belong to this department
                courses = db.session.query(
                    Course.course_name
                ).filter(
                    Course.department_id == department_id
                ).all()

                # Extract course names from the query results
                course_names = [course.course_name for course in courses]

                return {
                    "id": department_data.id,
                    "name": department_data.course_name,
                    "submitted_by": department_data.submitted_by,
                    "updated_at": department_data.updated_at,
                    "courses": course_names
                }, 200
            return {"message": "Department not found"}, 404

        # Get all departments and their related courses
        departments = db.session.query(Department).all()

        response = []
        for department_data in departments:
            department_id = department_data.id

            # Query all courses that belong to this department
            courses = db.session.query(
                Course.course_name
            ).filter(
                Course.department_id == department_id
            ).all()

            # Extract course names from the query results
            course_names = [course.course_name for course in courses]

            # Add department data to response
            response.append({
                "id": department_id,
                "department_name": department_data.department_name,
                "submitted_by": department_data.submitted_by,
                "updated_at": department_data.updated_at,
                "courses": course_names
            })

        return response, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('department_name', required=True)
        parser.add_argument('submitted_by', required=True)
        args = parser.parse_args()

        new_department = Department(department_name=args['department_name'], submitted_by=args['submitted_by']) 
        db.session.add(new_department)
        db.session.commit()
        return {"message": "Department created successfully"}, 201

    def put(self, department_id):
        department = Department.query.get(department_id)
        if not department:
            return {"message": "Department not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('department_name', required=False)
        parser.add_argument('submitted_by', required=False)
        args = parser.parse_args()

        if args['department_name']:
            department.department_name = args['department_name']
        if args['submitted_by']:
            department.submitted_by = args['submitted_by']
        
        db.session.commit()
        return {"message": "Department updated successfully"}, 200

    def delete(self, department_id): 
        department = Department.query.get(department_id)
        if not department:
            return {"message": "Department not found"}, 404

        db.session.delete(department)
        db.session.commit()
        return {"message": "Department deleted successfully"}, 200
    

class CourseResource(Resource):
    def get(self, course_id=None):
        if course_id:
            course = Course.query.get(course_id)
            if course:
                return {
                    "id": course.id,
                    "course_name": course.course_name,
                    "department_id": course.department_id,
                    "lecture_hours": course.lecture_hours,
                    "submitted_by": course.submitted_by
                }, 200
            return {"message": "Course not found"}, 404
        courses = Course.query.all()
        return [
            {
                "id": course.id,
                "course_name": course.course_name,
                "department_id": course.department_id,
                "lecture_hours": course.lecture_hours,
                "submitted_by": course.submitted_by
            } for course in courses
        ], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course_name', required=True)
        parser.add_argument('department_id', type=int, required=True)
        parser.add_argument('lecture_hours', type=int, required=True)
        parser.add_argument('submitted_by', required=True)
        args = parser.parse_args()

        new_course = Course(
            course_name=args['course_name'],
            department_id=args['department_id'],
            lecture_hours=args['lecture_hours'],
            submitted_by=args['submitted_by']
        )
        db.session.add(new_course)
        db.session.commit()
        return {"message": "Course created successfully"}, 201

    def put(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('course_name', required=False)
        parser.add_argument('department_id', type=int, required=False)
        parser.add_argument('lecture_hours', type=int, required=False)
        parser.add_argument('submitted_by', required=False)
        args = parser.parse_args()

        if args['course_name']:
            course.course_name = args['course_name']
        if args['department_id'] is not None:
            course.department_id = args['department_id']
        if args['lecture_hours'] is not None:
            course.lecture_hours = args['lecture_hours']
        if args['submitted_by']:
            course.submitted_by = args['submitted_by']

        db.session.commit()
        return {"message": "Course updated successfully"}, 200

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if not course:
            return {"message": "Course not found"}, 404

        db.session.delete(course)
        db.session.commit()
        return {"message": "Course deleted successfully"}, 200

class StudentResource(Resource):
    def get(self, student_id=None):
        if student_id:
            # Get a specific student and their department and courses
            student_data = db.session.query(Student).filter(Student.id == student_id).first()

            if student_data:
                # Retrieve the student's department and related courses
                department = db.session.query(Department).filter(
                    Department.id == student_data.department_id
                ).first()

                # Get all courses associated with this department
                courses = db.session.query(Course.course_name).filter(
                    Course.department_id == student_data.department_id
                ).all()

                # Extract course names from query results
                course_names = [course.course_name for course in courses]

                return {
                    "id": student_data.id,
                    "name": student_data.full_name,
                    "department_name": department.department_name if department else None,
                    "courses": course_names
                }, 200

            return {"message": "Student not found"}, 404
        students = db.session.query(Student).all()
        response = []

        for student_data in students:
            department = db.session.query(Department).filter(
                Department.id == student_data.department_id
            ).first()

            # Get all courses associated with this department
            courses = db.session.query(Course.course_name).filter(
                Course.department_id == student_data.department_id
            ).all()

            # Extract course names from query results
            course_names = [course.course_name for course in courses]

            # Append each student's info to the response
            response.append({
                "id": student_data.id,
                "name": student_data.full_name,
                "department_name": department.department_name if department else None,
                "courses": course_names
            })

        return response, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('full_name', required=True)
        parser.add_argument('department_id', type=int, required=True)
        parser.add_argument('submitted_by', required=True)
        args = parser.parse_args()

        new_student = Student(
            full_name=args['full_name'],
            department_id=args['department_id'],
            submitted_by=args['submitted_by']
        )
        db.session.add(new_student)
        db.session.commit()
        return {"message": "Student created successfully"}, 201

    def put(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('full_name', required=False)
        parser.add_argument('department_id', type=int, required=False)
        parser.add_argument('submitted_by', required=False)
        args = parser.parse_args()

        if args['full_name']:
            student.full_name = args['full_name']
        if args['department_id'] is not None:
            student.department_id = args['department_id']
        if args['submitted_by']:
            student.submitted_by = args['submitted_by']

        db.session.commit()
        return {"message": "Student updated successfully"}, 200

    def delete(self, student_id):
        student = Student.query.get(student_id)
        if not student:
            return {"message": "Student not found"}, 404

        db.session.delete(student)
        db.session.commit()
        return {"message": "Student deleted successfully"}, 200

class AttendanceLogResource(Resource):
    def get(self, log_id=None):
        print("/nhello/n")
        if log_id:
            logs = db.session.query(
                AttendanceLog,
                Student.full_name,
                Department.department_name
                ).join(
                Student, AttendanceLog.student_id == Student.id
                ).join(
                Department, Student.department_id == Department.id
                ).filter(
                AttendanceLog.id == log_id
                ).first()

            student_id=logs.AttendanceLog.student_id

            courses = db.session.query(
                Course.course_name
                ).join(
                Department, Course.department_id == Department.id
                ).join(
                Student, Student.department_id == Department.id
                ).filter(
                Student.id == student_id
                ).all()

            course_names = [course.course_name for course in courses]
            print("/n/n studentid /n/n", AttendanceLog.student_id)

            if logs:
                return{
                    "id": logs.AttendanceLog.id,
                    "student_name": logs.full_name,
                    "department_name": logs.department_name,
                    "courses": course_names,
                    "attended_at": logs.AttendanceLog.attended_at,
                }, 200

            return {"message": "Attendance log not found"}, 404

        attendance_log = db.session.query(AttendanceLog).all()

        response = []
        for attendance in attendance_log:
            student_id = attendance.student_id

            logs = db.session.query(
            AttendanceLog,
            Student.full_name,
            Department.department_name
            ).join(
            Student, AttendanceLog.student_id == Student.id
            ).join(
            Department, Student.department_id == Department.id
            ).first()

            # Query all courses that belong to this department
            courses = db.session.query(
            Course.course_name
            ).join(
            Department, Course.department_id == Department.id
            ).join(
            Student, Student.department_id == Department.id
            ).filter(
            Student.id == student_id
            ).all()

            # Extract course names from the query results
            course_names = [course.course_name for course in courses]

            # Add department data to response
            response.append({
                "id": attendance.id,
                "student_name": logs.full_name,
                "department_name": logs.department_name,
                "courses": course_names,
                "attended_at": logs.AttendanceLog.attended_at,
            })

        return response, 200

        



    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', type=int, required=True)
        parser.add_argument('student_id', type=int, required=True)
        args = parser.parse_args()

        new_log = AttendanceLog(
            course_id=args['course_id'],
            student_id=args['student_id']
        )
        db.session.add(new_log)
        db.session.commit()
        return {"message": "Attendance log created successfully"}, 201

class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            # Get a specific user and their submitted courses
            user_data = db.session.query(User).filter(User.id == user_id).first()

            if user_data:
                # Retrieve all courses submitted by this user
                courses = db.session.query(Course.course_name).filter(Course.submitted_by == user_data.id).all()

                # Extract course names from query results
                course_names = [course.course_name for course in courses]

                return {
                    "id": user_data.id,
                    "name": user_data.name,
                    "submitted_courses": course_names
                }, 200

            return {"message": "User not found"}, 404

        # Get all users and their submitted courses
        users = db.session.query(User).all()
        response = []

        for user_data in users:
            # Retrieve all departments submitted by this user
            departments = db.session.query(Department.department_name).filter(Department.submitted_by == user_data.name).all()

            # Extract department names from query results
            department_names = [department.department_name for department in departments]

            # Append each user's info to the response
            response.append({
                "id": user_data.id,
                "name": user_data.name,
                "submitted_departments": department_names
            })

        return response, 200
        

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('username', required=True)
        parser.add_argument('password', required=True)
        parser.add_argument('submitted_by', required=True)
        args = parser.parse_args()

        new_user = User(
            type=args['type'],
            name=args['name'],
            username=args['username'],
            password=args['password'],
            submitted_by=args['submitted_by']
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('type', required=False)
        parser.add_argument('name', required=False)
        parser.add_argument('username', required=False)
        parser.add_argument('password', required=False)
        parser.add_argument('submitted_by', required=False)
        args = parser.parse_args()

        if args['type']:
            user.type = args['type']
        if args['name']:
            user.name = args['name']
        if args['username']:
            user.username = args['username']
        if args['password']:
            user.password = args['password']
        if args['submitted_by']:
            user.submitted_by = args['submitted_by']

        db.session.commit()
        return {"message": "User updated successfully"}, 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200    