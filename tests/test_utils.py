import models

def clearDatabase(db):
  db.session.query(models.Score).delete()
  db.session.query(models.Criterion).delete()
  db.session.query(models.Category).delete()
  db.session.commit()
