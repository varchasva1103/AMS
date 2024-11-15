from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(255), nullable=False)
    submitted_by = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    lecture_hours = db.Column(db.Integer)
    submitted_by = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime)
    department = db.relationship('Department', backref='courses')

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    submitted_by = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime)
    department = db.relationship('Department', backref='students')

class AttendanceLog(db.Model):
    __tablename__ = 'attendance_log'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    attended_at = db.Column(db.DateTime)

    course = db.relationship('Course', backref='attendance_logs')
    student = db.relationship('Student', backref='attendance_logs')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    submitted_by = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime)