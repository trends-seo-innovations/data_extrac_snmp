from backend_api.app.models import db

class SnmpPoller(db.Model):
    __tablename__ = 'snmp_poller'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(50), nullable=False)
    subnet = db.Column(db.Integer, nullable=True)
    community_string = db.Column(db.String(255), nullable=False)
    interval = db.Column(db.Integer, nullable=False)
    table_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, nullable=True, default=0)
    pid = db.Column(db.Integer, nullable=True, default=0)



    