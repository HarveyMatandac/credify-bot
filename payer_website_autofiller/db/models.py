from sqlalchemy import Column, String
from payer_website_autofiller.db.database import Base


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(String(100), primary_key=True)
    run_id = Column(String(50))
    status = Column(String(20))
