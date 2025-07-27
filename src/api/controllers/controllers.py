from services.analytics_service import LearningAnalyticsService

class AnalyticsController:
    def __init__(self):
        self.analytics_service = LearningAnalyticsService()
    
    def get_student_analysis(self, student_id):
        return self.analytics_service.analyze_student_performance(student_id)
    
    def get_class_insights(self, class_id):
        return self.analytics_service.generate_class_insights(class_id)