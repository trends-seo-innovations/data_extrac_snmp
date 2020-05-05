from backend_api.app.models import db

class Blacklist(db.Model):
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    snmp_poller_id = db.Column(db.Integer, db.ForeignKey('snmp_poller.id'))
    ip_address = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    system_description = db.Column(db.String(50), nullable=False)
    system_name = db.Column(db.String(50), nullable=False)

