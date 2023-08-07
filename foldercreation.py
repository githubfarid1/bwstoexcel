import os
from settings import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from dbclass import Doc, Department, Bundle, Base
# from pathlib import Path


engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()    
result = session.query(Department).all()
result = session.query(Doc).join(Bundle).join(Department).filter(Department.link == "irigasi").all()
for res in result:
    boxfolder = os.path.join(STARTFOLDER, "{}-box-{}".format(res.Bundle.Department.link, res.Bundle.box_number))
    isExist = os.path.exists(boxfolder)
    if not isExist:
        os.mkdir(boxfolder)

    docnumberfolder = os.path.join(boxfolder, str(res.doc_number))
    try:
        os.mkdir(docnumberfolder)
        print(docnumberfolder, "created")
    except:
        pass
