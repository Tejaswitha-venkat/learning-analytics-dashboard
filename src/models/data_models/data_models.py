from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, Boolean, Enum, create_engine
from sqlalchemy.orm import declarative_base, relationship, validates, sessionmaker
from datetime import datetime
import enum

# Create database engine
engine = create_engine('sqlite:///educational_analytics.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ActivityType(enum.Enum):
    LOGIN = "login"
    ASSIGNMENT_SUBMISSION = "assignment_submission"
    COURSE_ACCESS = "course_access"
    RESOURCE_DOWNLOAD = "resource_download"
    DISCUSSION_POST = "discussion_post"

# Association tables
student_course = Table('student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id', ondelete='CASCADE')),
    Column('course_id', Integer, ForeignKey('courses.id', ondelete='CASCADE'))
)

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    grade_level = Column(Integer, nullable=False)
    average_score = Column(Float, default=0.0)
    attendance_rate = Column(Float, default=0.0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    risk_score = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    courses = relationship("Course", secondary=student_course, back_populates="students")
    assignments = relationship("Assignment", back_populates="student", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="student", cascade="all, delete-orphan")

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address")
        return email

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    courses = relationship("Course", back_populates="teacher", cascade="all, delete-orphan")

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email address")
        return email

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    teacher = relationship("Teacher", back_populates="courses")
    students = relationship("Student", secondary=student_course, back_populates="courses")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

    @validates('end_date')
    def validate_end_date(self, key, end_date):
        if end_date <= self.start_date:
            raise ValueError("End date must be after start date")
        return end_date

class Assignment(Base):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    course_id = Column(Integer, ForeignKey('courses.id', ondelete='CASCADE'))
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    score = Column(Float)
    max_score = Column(Float, nullable=False)
    submitted_date = Column(DateTime)
    due_date = Column(DateTime, nullable=False)
    is_submitted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="assignments")
    course = relationship("Course", back_populates="assignments")

    @validates('score')
    def validate_score(self, key, score):
        if score > self.max_score:
            raise ValueError("Score cannot exceed maximum score")
        return score

class Activity(Base):
    __tablename__ = 'activities'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))
    activity_type = Column(Enum(ActivityType), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Integer)  # in minutes
    details = Column(String(500))
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="activities")

    @validates('duration')
    def validate_duration(self, key, duration):
        if duration and duration < 0:
            raise ValueError("Duration cannot be negative")
        return duration

def init_db():
    Base.metadata.create_all(engine)
    
def get_session():
    return Session()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")

    session = get_session()

    try:
        teacher = Teacher(
            name="John Smith",
            email="john.smith@school.edu",
            department="Mathematics"
        )
        session.add(teacher)

        course = Course(
            name="Advanced Mathematics",
            description="Advanced mathematics course for grade 10",
            teacher=teacher,
            start_date=datetime.now(),
            end_date=datetime.now().replace(year=datetime.now().year + 1)
        )
        session.add(course)

        student = Student(
            name="Jane Doe",
            email="jane.doe@student.edu",
            grade_level=10
        )
        session.add(student)

        student.courses.append(course)

        assignment = Assignment(
            student=student,
            course=course,
            title="Calculus Basics",
            description="Introduction to derivatives",
            max_score=100.0,
            due_date=datetime.now().replace(day=datetime.now().day + 7)
        )
        session.add(assignment)

        activity = Activity(
            student=student,
            activity_type=ActivityType.LOGIN,
            duration=30,
            details="Initial login",
            ip_address="127.0.0.1"
        )
        session.add(activity)

        session.commit()
        print("Sample data created successfully!")

    except Exception as e:
        print(f"Error creating sample data: {e}")
        session.rollback()
    finally:
        session.close()