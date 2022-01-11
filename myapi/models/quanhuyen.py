from flask.signals import _FakeSignal
from myapi.extensions import db
from sqlalchemy.dialects.postgresql import UUID



class Quanhuyen(db.Model):

    __tablename__="quanhuyen"
    id = db.Column(UUID , primary_key=True)
    ma = db.Column(db.String(300))
    ten = db.Column(db.String(300))
    tenkhongdau = db.Column(db.String(300))
    ten_tieng_anh = db.Column(db.String(300),)
    loai = db.Column(db.String(300))
    tinhthanh_id = db.Column(UUID, db.ForeignKey("tinhthanh.id"))
    active = db.Column(db.String,)
    created_at = db.Column(db.String(300) )
    created_by = db.Column(db.String(300))
    updated_at = db.Column(db.String(300))
    updated_by = db.Column(db.String(300))
    deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.String(300))
    deleted_by = db.Column(db.String(300))


    def __repr__(self):
        return
    
    def __init__(self, ten=None):
        self.ten = ten

    def __str__(self):
        return