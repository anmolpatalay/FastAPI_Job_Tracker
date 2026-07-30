'''
users            id, email (unique), hashed_password, created_at
companies        id, user_id (FK), name, website, notes
applications     id, user_id (FK), company_id (FK), role_title,
                 status (ENUM: applied/screening/interviewing/offer/rejected/withdrawn),
                 applied_date, job_url, resume_version, notes, created_at, updated_at
interviews       id, application_id (FK), round_name, scheduled_at, outcome, notes
status_history   id, application_id (FK), old_status, new_status, changed_at
'''
from datetime import datetime
from database import BASE
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey,TIMESTAMP,Enum,DateTime,Date
status_enums = ('applied','screening','interviewing','offer','rejected','withdrawn')

class Users(BASE):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String(30),unique=True,nullable=False)
    hashed_password = Column(String(100))
    created_at = Column(TIMESTAMP,default=datetime.now())

class Companies(BASE):
    __tablename__ = "companies"
    company_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    company_name = Column(String(30))
    note = Column(String(30))

class Applications(BASE):
    __tablename__ = "applications"
    application_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey(Users.id))
    comapany_id = Column(Integer,ForeignKey('companies.company_id'))
    role_title = Column(String(30))
    status = Column(Enum(*status_enums), nullable=False)
    applied_date= Column(Date)
    job_url = Column(String(250))


class Interviews(BASE):
    __tablename__ = "interviews"
    interview_id = Column(Integer,primary_key=True,index=True)
    application_id = Column(Integer,ForeignKey('applications.application_id'))
    round_name = Column(String(20))
    scheduled_at = Column(DateTime)




