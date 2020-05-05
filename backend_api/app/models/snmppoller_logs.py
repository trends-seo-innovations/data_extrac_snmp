from backend_api.app.models import db


class SnmpPollerLogs(db.Model):
    __tablename__ = 'snmp_poller_logs'
    id = db.Column(db.Integer, primary_key=True)
    snmp_poller_id = db.Column(db.Integer)
    log_level = db.Column(db.String(50),nullable=True)
    description = db.Column(db.String(600), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True) 
