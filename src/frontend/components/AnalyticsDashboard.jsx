import React, { useState, useEffect } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar, ResponsiveContainer
} from 'recharts';

const AnalyticsDashboard = () => {
  const [studentData, setStudentData] = useState(null);
  const [classData, setClassData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [studentResponse, classResponse] = await Promise.all([
          fetch('http://localhost:5000/api/student/1/analysis'),
          fetch('http://localhost:5000/api/class/1/insights')
        ]);

        const studentData = await studentResponse.json();
        const classData = await classResponse.json();

        setStudentData(studentData);
        setClassData(classData);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch analytics data');
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading analytics...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="analytics-dashboard">
      <div className="student-section">
        <h2>Student Performance</h2>
        <div className="metrics-grid">
          <div className="metric-card">
            <h3>Average Score</h3>
            <p>{studentData?.performance_metrics?.average_score}%</p>
          </div>
          <div className="metric-card">
            <h3>Attendance Rate</h3>
            <p>{studentData?.performance_metrics?.attendance_rate}%</p>
          </div>
          <div className="metric-card">
            <h3>Risk Score</h3>
            <p>{studentData?.risk_score}</p>
          </div>
        </div>

        <div className="performance-chart">
          <h3>Performance Trends</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={studentData?.performance_trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="score" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="class-section">
        <h2>Class Insights</h2>
        <div className="class-stats">
          <div className="stat-card">
            <h3>Total Students</h3>
            <p>{classData?.class_stats?.total_students}</p>
          </div>
          <div className="stat-card">
            <h3>Class Average</h3>
            <p>{classData?.class_stats?.average_score.toFixed(2)}%</p>
          </div>
          <div className="stat-card">
            <h3>At Risk Students</h3>
            <p>{classData?.class_stats?.at_risk_students}</p>
          </div>
        </div>

        <div className="completion-chart">
          <h3>Assignment Completion Rate</h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={[{ rate: classData?.class_stats?.assignment_completion_rate * 100 }]}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="rate" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;