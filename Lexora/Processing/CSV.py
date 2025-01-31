import pandas as pd
import google.generativeai as genai

class CSVProcessor:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)

    def process_csv(self, path):
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".xlsx") or path.endswith(".xls"):
            df = pd.read_excel(path)
        else:
            raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")
        
        text_data = df.select_dtypes(include=['object'])
        all_text = text_data.values.flatten().tolist()
        all_text = [str(text) for text in all_text if pd.notna(text)]
        all_text.append(df.describe().to_string())
        content = ' '.join(all_text)
        
        prompt = f"""
        Analyze the following dataset and provide a comprehensive summary of the data:
        {content}
        """
        
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        description = response.parts[0].text.strip()
        return description

# Usage
# api_key = "AIzaSyBkXXtG5XeopoPisjR0LGqFdNcy3F_a8eo"
# csv_processor = CSVProcessor(api_key)
# csv_path = "D:\Hilti_Hackathon\Hilti_Hackathon\Target_Folder\Target_Folder\Additional_Files\CSVs\Employee-Management-Data-for-Analysis.xlsx"
# extracted_text = csv_processor.process_csv(csv_path)
# print(extracted_text)
