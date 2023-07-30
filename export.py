from settings import *
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from dbclass import Doc, Department, Bundle, Base
import xlwings as xw
from xlwings.constants import LineStyle, Background, RgbColor, VAlign, HAlign
import sys
import settings

xlbook = xw.Book()
xlsheet = xlbook.sheets[0]
wbsource = xw.Book("template.xlsx")
wssource = wbsource.sheets['template']

engine = create_engine('mysql+pymysql://{}:{}@localhost:{}/{}'.format(USER, PASSWORD, PORT, DBNAME) , echo=False)
Session = sessionmaker(bind = engine)
session = Session()    
result = session.query(Department).all()
for res in result:
    wssource.api.Copy(Before=xlsheet.api)
xlbook.sheets[-1].delete()
for idx, sheet in enumerate(xlbook.sheets):
    sheet.name = result[idx].name
wbsource.close()
xlbook.sheets.add("setting", after=xlbook.sheets[-1])
xlbook.sheets["setting"]['A1'].value = os.path.join("D:\\", "media") + "\\"
for sheet in xlbook.sheets:
    if sheet.name == "setting":
        continue

    result = session.query(Doc).join(Bundle).join(Department).filter(Department.name == sheet.name).all()
    print(sheet.name, "Processing..", end=" ", flush=True)
    i = 7
    curbox = result[0].Bundle.box_number
    curbundle = result[0].Bundle.bundle_number
    isfirst = True
    for res in result:
        if isfirst:
            isfirst = False
            sheet['{}{}'.format('A', i)].value = res.Bundle.box_number
            sheet['{}{}'.format('B', i)].value = res.Bundle.bundle_number
            sheet['{}{}'.format('C', i)].value = res.doc_number
            sheet['{}{}'.format('D', i)].value = res.Bundle.code
            sheet['{}{}'.format('E', i)].value = res.Bundle.title
            sheet['{}{}'.format('F', i)].value = res.description
            sheet['{}{}'.format('G', i)].value = res.Bundle.year
            sheet['{}{}'.format('H', i)].value = res.doc_count
            sheet['{}{}'.format('I', i)].value = res.Bundle.orinot
        else:
            if curbox != res.Bundle.box_number:
                curbox = res.Bundle.box_number
                sheet['{}{}'.format('A', i)].value = res.Bundle.box_number
            else:
                sheet['{}{}'.format('A', i)].value = "" 
            if curbundle != res.Bundle.bundle_number:
                curbundle = res.Bundle.bundle_number
                sheet['{}{}'.format('B', i)].value = res.Bundle.bundle_number
                sheet['{}{}'.format('D', i)].value = res.Bundle.code
                sheet['{}{}'.format('E', i)].value = res.Bundle.title
                sheet['{}{}'.format('G', i)].value = res.Bundle.year
                sheet['{}{}'.format('I', i)].value = res.Bundle.orinot
            else:
                sheet['{}{}'.format('B', i)].value = ""
                sheet['{}{}'.format('D', i)].value = ""
                sheet['{}{}'.format('E', i)].value = ""
                sheet['{}{}'.format('G', i)].value = ""
                sheet['{}{}'.format('I', i)].value = ""
            sheet['{}{}'.format('C', i)].value = res.doc_number
            sheet['{}{}'.format('F', i)].value = res.description
            sheet['{}{}'.format('H', i)].value = res.doc_count
        if res.filesize is not None:
            filelocation = os.path.join(settings.APP_NAME, res.Bundle.Department.link, str(res.Bundle.box_number), str(res.doc_number) + ".pdf")
            sheet['{}{}'.format('F', i)].color = RgbColor.rgbLightGreen
            sheet['{}{}'.format('J', i)].color = RgbColor.rgbLightGreen
            sheet['{}{}'.format('J', i)].value = '=HYPERLINK(CONCATENATE(setting!A1, "{}")'.format(filelocation) + ', "LIHAT")'
        i += 1
    cells = sheet.range('A7', 'J{}'.format(i))
    cells.api.Borders.LineStyle = LineStyle.xlContinuous
    cells.api.VerticalAlignment = VAlign.xlVAlignCenter
    cells = sheet.range('A7', 'D{}'.format(i))
    cells.api.HorizontalAlignment = HAlign.xlHAlignCenter
    cells = sheet.range('G7', 'J{}'.format(i))
    cells.api.HorizontalAlignment = HAlign.xlHAlignCenter
    xlsheet.save(os.path.join(settings.SAVE_LOCATION, settings.FILENAME))
    xlsheet.close()
    print("Success")