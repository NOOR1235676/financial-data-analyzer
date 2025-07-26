import pandas as pd

class ExcelProcessor:
    def __init__(self):
        self.files = {}

    def load_files(self, file_paths):
        for path in file_paths:
            try:
                self.files[path] = pd.ExcelFile(path, engine='openpyxl')
            except Exception as e:
                print(f"Error loading {path}: {e}")

    def get_sheet_info(self):
        info = {}
        for file, xls in self.files.items():
            info[file] = {
                'sheet_names': xls.sheet_names,
                'sheet_info': {}
            }
            for sheet in xls.sheet_names:
                try:
                    df = xls.parse(sheet)
                    info[file]['sheet_info'][sheet] = {
                        'rows': df.shape[0],
                        'columns': df.shape[1],
                        'column_names': df.columns.tolist()
                    }
                except Exception as e:
                    info[file]['sheet_info'][sheet] = {'error': str(e)}
        return info

    def extract_data(self, file, sheet_name):
        try:
            return self.files[file].parse(sheet_name)
        except Exception as e:
            print(f"Error extracting sheet {sheet_name} from {file}: {e}")
            return pd.DataFrame()

    def preview_data(self, file, sheet_name, rows=5):
        df = self.extract_data(file, sheet_name)
        return df.head(rows)
