import openpyxl

global data,sheet
uid = "5513020355"

data = openpyxl.load_workbook('E:\\PYTHON临时\\评论excel\\5513020355.xlsx') #读取格式转换后的文件三  .format(uid)
sheet = book.create_sheet(uid)

