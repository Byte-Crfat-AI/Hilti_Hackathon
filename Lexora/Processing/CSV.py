import pandas as pd
import google.generativeai as genai

class CSV:
    def __init__(self):
        genai.configure(api_key="YOUR_API_KEY")
    def process_csv(path):
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
        description = response.choices[0].text.strip()
        return description


# Example
# csv_path = r'D:\Hilti_Hackathon\Hilti_Hackathon\Target_Folder\Target_Folder\Additional_Files\CSVs\Employee-Management-Data-for-Analysis.xlsx'
# extracted_text = CSV.process_csv(csv_path)
# print(extracted_text)
