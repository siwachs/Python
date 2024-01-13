from openpyxl import load_workbook


def delete_sheet_by_name(file_path, sheet_name):
    wb = load_workbook(file_path)

    if sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        wb.remove(sheet)
        wb.save(file_path)
        print(f"The sheet '{sheet_name}' has been deleted.")
    else:
        print(f"The sheet '{sheet_name}' does not exist in the workbook.")


file_path = r'E:\Projects\Python\Delete Sheet\1.xlsx'
sheet_name_to_delete = 'Evaluation Warning'
delete_sheet_by_name(file_path, sheet_name_to_delete)
