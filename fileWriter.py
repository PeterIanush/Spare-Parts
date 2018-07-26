import xlwt
from PyQt5.QtWidgets import QFileDialog


def savefile(tableWidget, headers):
    filename = QFileDialog.getSaveFileName(None, 'Save File', '', '.xls(*.xls)')
    wbk = xlwt.Workbook(encoding="utf-8")
    sheet = wbk.add_sheet('sheet1', cell_overwrite_ok=True)
    writeTosheet(sheet=sheet, table=tableWidget, headers=headers)
    wbk.save(filename[0])


def writeTosheet(sheet, table, headers):
    for currentColumn, h in enumerate(headers):
        sheet.write(0, currentColumn, h)
    for currentColumn in range(0, table.columnCount()):
        for currentRow in range(1, table.rowCount() + 1):
            teext = table.item(currentRow - 1, currentColumn).text()
            sheet.write(currentRow, currentColumn, teext)