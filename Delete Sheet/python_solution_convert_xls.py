import xlwings as xw


def convert_to_xlsx(file_path, output_path):
    try:
        app = xw.App(visible=False)  # Open Excel in the background
        workbook = app.books.open(file_path)
        workbook.save(output_path)
        workbook.close()
        app.quit()

        print(f"Conversion completed. File saved at: {output_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    input_file_path = r'E:\Projects\Python\Delete Sheet\1.xls'
    output_file_path = r'E:\Projects\Python\Delete Sheet\1_converted.xlsx'
    convert_to_xlsx(input_file_path, output_file_path)
