from sqlalchemy import Column, String, Text, Integer, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


job_tag_relation = Table(
    "job_tag_relation", Base.metadata,
    Column('job_id', Integer, ForeignKey("jobs.id"), primary_key=True),
    Column('tag_id', Integer, ForeignKey("tags.id"), primary_key=True)
)


class Job(Base):
    __tablename__="jobs"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    source = Column(String(256), nullable=False)
    url = Column(String(256), nullable=False, unique=True)
    title = Column(String(164), nullable=False)
    content = Column(Text, nullable=False)
    remote = Column(String(64), nullable=False)
    company = Column(String(64), nullable=False)
    salery = Column(Integer, nullable=True)
    time = Column(String(64), nullable=True)
    eng_level = Column(String(65), nullable=True)
    published_at = Column(DateTime, nullable=False)
    company_link = Column(String(256),nullable=True)

    tags = relationship(
        "Tag",
        secondary=job_tag_relation,
        back_populates="jobs"
    )


class Tag(Base):
    __tablename__="tags"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(64), unique=True, nullable=False)

    jobs = relationship(
        'Job',
        secondary=job_tag_relation,
        back_populates='tags'
    ) 

