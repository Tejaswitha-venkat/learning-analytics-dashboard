from flask import Flask
from flask_cors import CORS
from api.routes.analytics_routes import analytics_bp
from models.data_models.data_models import init_db

app = Flask(__name__)
CORS(app)  # Enable CORS
app.register_blueprint(analytics_bp, url_prefix='/api')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)  # Change port back to 5000