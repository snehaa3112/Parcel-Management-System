from models import db, Log

def add_log(parcel_id, status):
    log = Log(parcel_id=parcel_id, status=status)
    db.session.add(log)
    db.session.commit()
