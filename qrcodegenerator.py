import os
from settings import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from dbclass import Doc, Department, Bundle, Base
# from pathlib import Path
import qrcode

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()    
deps = session.query(Department).all()
boxnumbers = []
for res in deps:
    boxes = session.query(Bundle).filter(Bundle.department_id == res.id).all()

    boxnumbers = set([box.box_number for box in boxes])
    for boxnumber in boxnumbers:
        qrcodefile = os.path.join(QRCODELOCATION, "{}-box-{}.png".format(res.link, boxnumber))
        isExist = os.path.exists(qrcodefile)
        if not isExist:
            text = "/alihmedia_inactive/boxsearch/{}/{}".format(res.link, boxnumber)
            qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=5,
                    border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")            
            # img = qrcode.make(text)
            img.save(qrcodefile)
            print(text, "created")
    
    
    break
# print(boxnumbers)
    # boxfolder = os.path.join(STARTFOLDER, "{}-box-{}".format(res.Bundle.Department.link, res.Bundle.box_number))
    # isExist = os.path.exists(boxfolder)
    # if not isExist:
    #     os.mkdir(boxfolder)

    # docnumberfolder = os.path.join(boxfolder, str(res.doc_number))
    # try:
    #     os.mkdir(docnumberfolder)
    #     print(docnumberfolder, "created")
    # except:
    #     pass
