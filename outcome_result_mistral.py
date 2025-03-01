import os
import logging
import pandas as pd
import torch
import re
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import unicodedata

# Force Ollama to use CUDA if available
os.environ["OLLAMA_ACCELERATOR"] = "cuda"

# Check if CUDA is available
if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available, using CPU instead.")

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Toggle to process only the top 10 rows
PROCESS_TOP_n = False

def load_data(file_path):
    """Load CSV file into a Pandas DataFrame with proper encoding."""
    return pd.read_csv(file_path, encoding="utf-8")

def normalize_text(text):
    """Normalize text to handle different encodings and fix misencoded emojis."""
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("âœ…", "✅").replace("âœ•", "❌").replace("✘", "❌")  # Fix misencoded characters
    return text

def extract_betting_result(comment_text):
    """Extract win/loss/push result from comment_text, ensuring correct emoji recognition."""
    if pd.isna(comment_text):
        return ""
    
    comment_text = normalize_text(comment_text)
    lines = comment_text.lower().split("\n")
    for line in lines:
        if "last potd" in line:
            continue  # Skip processing if "Last POTD" is mentioned
        if re.search(r"\b(win|✅)\b", line):
            return "Win"
        elif re.search(r"\b(loss|❌|✘)\b", line):
            return "Loss"
        elif "push" in line:
            return "Push"
    
    return ""

def process_comments(df):
    """Extract structured data from all comments using multithreading and updating progress bar in real-time."""
    structured_data = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = list(executor.submit(extract_betting_result, comment) for comment in df["Comment_Text"])
        
        with tqdm(total=len(futures), desc="Processing Comments", unit="comment") as pbar:
            for future in futures:
                structured_data.append(future.result())
                pbar.update(1)
    
    return structured_data

def track_previous_pick_results(df):
    """Check if the same author mentions their previous pick and its result. Only check if the author match for the next day only."""
    df["Previous_Pick_Result"] = ""
    
    for i in range(1, len(df)):
        current_author = df.at[i, "Comment_Author"]
        previous_author = df.at[i - 1, "Comment_Author"]
        
        if current_author == previous_author:
            comment_text = df.at[i, "Comment_Text"]
            if any(x in comment_text.lower() for x in ["previous pick", "last pick", "yesterday", "prior pick"]):
                df.at[i, "Previous_Pick_Result"] = extract_betting_result(comment_text)
    
    return df

def main():
    # Define file paths
    input_file_path = "data/2024_llm_POTD_identified_clean.csv"
    output_file_path = "data/2024_result.csv"

    df = load_data(input_file_path)
    if df is None:
        logging.error("Failed to load data.")
        return
        
    if 'Comment_Text' not in df.columns or 'Comment_Author' not in df.columns:
        logging.error("Missing required columns in data.")
        return
    
    # Process only top 100 rows if enabled
    if PROCESS_TOP_n:
        df = df.head(100)
    
    # Extract results using multithreading
    df['Result'] = process_comments(df)
    
    # Track previous pick results
    df = track_previous_pick_results(df)
    
    # Save updated data
    df.to_csv(output_file_path, index=False)
    logging.info(f"Processed data saved to {output_file_path}")

if __name__ == "__main__":
    main()
