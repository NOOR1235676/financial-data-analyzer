import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.core.excel_processor import ExcelProcessor

def main():
    files = [
        "../data/sample/KH_Bank.XLSX",
        "../data/sample/Customer_Ledger_Entries_FULL.xlsx"
    ]

    processor = ExcelProcessor()
    processor.load_files(files)

    info = processor.get_sheet_info()
    for file, file_info in info.items():
        print(f"\n📁 File: {file}")
        print(f"📄 Sheets: {file_info['sheet_names']}")
        for sheet, meta in file_info['sheet_info'].items():
            print(f"  ▶ Sheet: {sheet}")
            if 'error' in meta:
                print(f"    ❌ Error reading sheet: {meta['error']}")
            else:
                print(f"    ✅ Rows: {meta['rows']}, Columns: {meta['columns']}")
                print(f"    🧾 Columns: {meta['column_names']}")

        # Preview
        if file_info['sheet_names']:
            preview = processor.preview_data(file, file_info['sheet_names'][0])
            print("\n🔍 Data Preview (first 5 rows):")
            print(preview)

if __name__ == "__main__":
    main()
