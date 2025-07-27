from models.data_models.data_models import Student, Course, Assignment, Activity, get_session
from datetime import datetime, timedelta
from sqlalchemy import func

class LearningAnalyticsService:
    def __init__(self):
        self.session = get_session()

    def analyze_student_performance(self, student_id):
        student = self.session.query(Student).get(student_id)
        if not student:
            return {"error": "Student not found"}

        # Calculate recent performance metrics
        recent_assignments = self.session.query(Assignment).filter(
            Assignment.student_id == student_id,
            Assignment.submitted_date >= datetime.now() - timedelta(days=30)
        ).all()

        recent_activities = self.session.query(Activity).filter(
            Activity.student_id == student_id,
            Activity.timestamp >= datetime.now() - timedelta(days=30)
        ).all()

        # Calculate analytics
        performance_metrics = {
            "average_score": student.average_score,
            "attendance_rate": student.attendance_rate,
            "risk_score": student.risk_score,
            "recent_assignments_completed": len([a for a in recent_assignments if a.is_submitted]),
            "recent_activity_count": len(recent_activities)
        }

        # Get performance trends
        performance_trends = [
            {
                "date": assignment.submitted_date.strftime("%Y-%m-%d"),
                "score": assignment.score
            }
            for assignment in recent_assignments 
            if assignment.submitted_date and assignment.score
        ]

        return {
            "student_info": {
                "name": student.name,
                "grade_level": student.grade_level,
                "email": student.email
            },
            "performance_metrics": performance_metrics,
            "performance_trends": performance_trends,
            "risk_score": student.risk_score
        }

    def generate_class_insights(self, class_id):
        course = self.session.query(Course).get(class_id)
        if not course:
            return {"error": "Course not found"}

        students = course.students
        assignments = course.assignments

        # Calculate class statistics
        class_stats = {
            "total_students": len(students),
            "average_score": sum(s.average_score for s in students) / len(students) if students else 0,
            "at_risk_students": len([s for s in students if s.risk_score > 0.7]),
            "assignment_completion_rate": len([a for a in assignments if a.is_submitted]) / len(assignments) if assignments else 0
        }

        return {
            "course_info": {
                "name": course.name,
                "teacher": course.teacher.name,
                "start_date": course.start_date.strftime("%Y-%m-%d"),
                "end_date": course.end_date.strftime("%Y-%m-%d")
            },
            "class_stats": class_stats
        }

    def calculate_risk_score(student_data):
        # Weights for different factors
        weights = {
            'performance': 0.4,
            'attendance': 0.3,
            'assignment_completion': 0.3
        }
        
        # Calculate individual scores
        performance_score = student_data.average_score / 100
        attendance_score = student_data.attendance_rate / 100
        completion_score = student_data.assignments_completed / student_data.total_assignments
        
        # Calculate weighted risk score
        risk_score = (
            (performance_score * weights['performance']) +
            (attendance_score * weights['attendance']) +
            (completion_score * weights['assignment_completion'])
        ) * 100
        
        return {
            'score': risk_score,
            'level': 'High' if risk_score < 60 else 'Medium' if risk_score < 80 else 'Low'
        }

    def analyze_performance_trends(scores_history):
        from scipy import stats
        
        # Calculate moving average
        window_size = 3
        moving_avg = [
            sum(scores_history[i:i+window_size]) / window_size 
            for i in range(len(scores_history) - window_size + 1)
        ]
        
        # Calculate trend slope
        x = range(len(scores_history))
        slope, _, _, _, _ = stats.linregress(x, scores_history)
        
        return {
            'trend': 'Improving' if slope > 0.1 else 'Declining' if slope < -0.1 else 'Stable',
            'moving_average': moving_avg
        }

    def aggregate_class_statistics(class_data):
        import numpy as np
        
        scores = [student.average_score for student in class_data]
        attendance = [student.attendance_rate for student in class_data]
        
        return {
            'average_score': np.mean(scores),
            'score_std_dev': np.std(scores),
            'median_score': np.median(scores),
            'attendance_rate': np.mean(attendance),
            'performance_distribution': np.histogram(scores, bins=5)[0].tolist()
        }