**# learning-analytics-dashboard**

## Project Overview
A full-stack educational analytics platform built with React frontend and Python/Flask backend for tracking and analyzing student performance data.

**project-2/**
├── src/
│   ├── api/                 # API endpoints and controllers
│   ├── models/
│   │   ├── data_models/     # Database models and schemas
│   │   └── ml_models/       # Machine learning models
│   ├── services/            # Business logic layer
│   ├── frontend/           # React components and styles
│   └── dashboards/         # Dashboard templates and styles
├── public/                 # Static assets
└── venv/                   # Python virtual environment

## Technology Stack
- Frontend : React.js with Recharts for data visualization
- Backend : Flask (Python)
- Database : SQLite with SQLAlchemy ORM
- Machine Learning : scikit-learn for predictive analytics
  ## Key Components
### Data Models
1. 
   Student Model
   
   - Tracks student information, grades, and activity
   - Includes risk assessment scores
   - Monitors attendance and performance metrics
2. 
   Teacher Model
   
   - Manages teacher profiles and department information
   - Links to courses and student groups
3. 
   Course Model
   
   - Handles course information and schedules
   - Manages student enrollments
   - Tracks assignments and resources
4. 
   Activity Model
   
   - Logs student interactions and engagement
   - Records different types of activities:
     - Login events
     - Assignment submissions
     - Course access
     - Resource downloads
     - Discussion participation
### Analytics Features
1. 
   Performance Tracking
   
   - Real-time grade monitoring
   - Attendance tracking
   - Activity analysis
2. 
   Risk Assessment
   
   - Predictive modeling using RandomForestClassifier
   - Early warning system for at-risk students
   - Automated risk score calculation
3. 
   Visualization Dashboard
   
   - Interactive charts and graphs
   - Performance trends
   - Comparative analytics
## Setup and Installation
1. 
   Install Python dependencies (use virtual environment)
2. 
   Install Node.js dependencies
3. 
   Initialize database
4. 
   Start Flask backend server
5. 
   Launch React frontend
   
## API Endpoints
- /api/student/<id>/analysis : Student-specific analytics
- /api/class/<id>/insights : Class-level performance data
- 
## Database Schema
The project uses SQLAlchemy with the following main tables:

- students
- teachers
- courses
- assignments
- activities
- 
## Frontend Components
- AnalyticsDashboard: Main dashboard interface
- Performance charts using Recharts
- Responsive design with CSS Grid/Flexbox
- 
## Machine Learning Integration
- Risk prediction model using Random Forest
- Feature scaling with StandardScaler
- Automated model training and prediction pipeline
- 
## Security Features
- Email validation
- Data validation checks
- Error handling for invalid inputs

## Development Guidelines
1. 
   Follow Python PEP 8 style guide
2. 
   Use React functional components with hooks
3. 
   Implement proper error handling
4. 
   Maintain data validation at all layers
