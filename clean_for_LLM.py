import pandas as pd
import re
import json

def load_csv(file_path):
    """Load CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def extract_date(post_title):
    match = re.search(r'(\d{1,2}/\d{1,2}/\d{2})', post_title)
    if match:
        return pd.to_datetime(match.group(1), format='%m/%d/%y').strftime('%m/%d/%Y')
    return None

def clean_comment_text(comment_text):
    """Pre-process comment text to remove unnecessary formatting."""
    if not isinstance(comment_text, str):
        return ""
    comment_text = re.sub(r'\*\*(.*?)\*\*', r'\1', comment_text)  # Remove Markdown bold (**text**)
    comment_text = re.sub(r'https?://\S+', '', comment_text)  # Remove links
    return comment_text

def clean_dataframe(df):
    """Drop Post_Date, remove unwanted comments, and drop short comments in one function."""
    df = df.drop(columns=['Post_Date'], errors='ignore')
    df = df[~df['Comment_Text'].str.contains(r'\[deleted\]|\[removed\]', na=False)]
    df['Comment_Text'] = df['Comment_Text'].apply(clean_comment_text)
    df = df[df['Comment_Text'].str.len() >= 250]
    return df

def preprocess_dataframe(df):
    """Apply all cleaning and transformations to the DataFrame."""
    df['Extracted_Date'] = df['Post_Title'].apply(extract_date)
    df = df.drop(columns=['Post_Title'], errors='ignore')
    df.insert(0, 'Extracted_Date', df.pop('Extracted_Date'))
    df = clean_dataframe(df)
    df['Comment_Text'] = df['Comment_Text'].apply(clean_comment_text)
    df['Comment_Length'] = df['Comment_Text'].apply(len)
    
    average_comment_length = df['Comment_Length'].mean()
    #print(f"Average Comment Length: {average_comment_length}")

    df = df.drop(columns=['Comment_Length'], errors='ignore')
    
    return df

def save_csv(df, output_path):
    """Save the cleaned DataFrame as a CSV file."""
    df.to_csv(output_path, index=False)
    print(f"CSV file saved as {output_path}")

def save_jsonl(df, output_path):
    """Save the cleaned DataFrame as a JSONL file."""
    df.to_json(output_path, orient='records', lines=True)
    print(f"JSONL file saved as {output_path}")

if __name__ == "__main__":
    file_path = "data/2024_POTD_top10each.csv"
    output_csv_path = "data/2024_POTD_cleaned.csv"
    output_jsonl_path = "data/2024_POTD_cleaned.jsonl"
    
    df = load_csv(file_path)
    df = preprocess_dataframe(df)
    save_csv(df, output_csv_path)
    save_jsonl(df, output_jsonl_path)
