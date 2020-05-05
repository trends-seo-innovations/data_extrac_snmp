from backend_api.app.models import db


class ApiLogs(db.Model):
    __tablename__ = 'api_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    api = db.Column(db.Integer)
    log_level = db.Column(db.String(50),nullable=True)
    description = db.Column(db.String(600), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True)
