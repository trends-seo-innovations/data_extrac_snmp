from backend_api.app.models import db

class SelectedOid(db.Model):
    __tablename__ = 'selected_oid'

    id = db.Column(db.Integer, primary_key=True)
    snmp_poller_id = db.Column(db.Integer, db.ForeignKey('snmp_poller.id'))
    oid_key = db.Column(db.String(50), nullable=False)