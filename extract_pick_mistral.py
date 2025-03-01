import pandas as pd
import ollama
import re
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

import os
import torch

# Force Ollama to use CUDA if available
os.environ["OLLAMA_ACCELERATOR"] = "cuda"

# Check if CUDA is available
if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available, using CPU instead.")

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_data(file_path):
    """Load CSV file into a Pandas DataFrame."""
    return pd.read_csv(file_path)

def extract_betting_info(comment_text):
    """Extract structured information from a betting comment using Mistral."""
    model_choice = "mistral"

    prompt = f"""
    Goal
    Extract structured betting information from a given betting comment, ensuring that key details, including odds and units, are correctly linked to the pick. The extraction must focus on "Today's Pick" or the most explicitly mentioned bet, while ignoring past results and unnecessary text.

    Return
    The output should be a JSON object with the following fields:

    Pick: The primary betting selection (required).
    Odds: The odds associated with the pick (required).
    Sport: The sport category (e.g., NFL, NBA) (required).
    Unit: The stake or risked amount in units (required).
    
    Warning
    If multiple picks exist, extract only "Today's Pick" or the most definitively stated bet.
    Ensure the odds are correctly linked to the extracted pick.
    Picks can be phrased informally; extract the most explicit bet.
    Ignore past bets (e.g., "Last Pick", "POTD Record", "Previous pick").
    Only extract the most definitive "Today's Pick" or the latest bet explicitly stated.
    If a field is missing, return "N/A".
    
    Context
    Picks can be formatted in various ways, including:
    "POTD: O31.5 Rush Yards - Tyler Huntley (-110 FanDuel; Risking 2.2u to win 2u)"
    "🔥 Best Bet: Both Teams 2+ Cards - NO"
    "🚀 Lock: City over 3.5 goals"
    "Pick: Josh Allen over 231.5 passing yards -120 (DraftKings)"
    "Today's Pick: Tallon Griekspoor vs Carlos Alcaraz | Griekspoor +5.5 games at -140. 2 units."
    Picks may include emojis or alternative formatting styles.
    The sport and unit size should be extracted if explicitly mentioned.
    
    ### Betting Comment:
    {comment_text}

    Return data in **JSON format**.
    """

    try:
        response = ollama.chat(model=model_choice, messages=[{"role": "user", "content": prompt}])
        extracted_data = json.loads(response["message"]["content"])
    except Exception as e:
        logging.warning(f"Error processing comment with {model_choice}: {e}")
        extracted_data = {
            "Pick": "N/A",
            "Odds": "N/A",
            "Sport": "N/A",
            "Unit": "1"
        }

    return extracted_data

def process_comments(df):
    """Extract structured data from all comments using multithreading."""
    structured_data = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(extract_betting_info, comment): comment for comment in df["Comment_Text"]}
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing Comments", unit="comment"):
            structured_data.append(future.result())
    
    return pd.DataFrame(structured_data)

def save_data(final_df, output_csv, output_json, output_jsonl):
    """Save the processed data to CSV, JSON, and JSONL files."""
    final_df.to_csv(output_csv, index=False)
    final_df.to_json(output_json, orient="records", indent=4)
    
    with open(output_jsonl, 'w') as jsonl_file:
        for record in final_df.to_dict(orient='records'):
            jsonl_file.write(json.dumps(record) + '\n')
    
    print(f"Saved to {output_csv}, {output_json}, and {output_jsonl}")

def main():
    file_path = "data/2024_POTD_cleaned.csv"
    output_csv = "currenttest/llm_POTD_identified.csv"
    output_json = "currenttest/llm_POTD_identified.json"
    output_jsonl = "currenttest/llm_POTD_identified.jsonl"
    
    df = load_data(file_path)
    structured_df = process_comments(df)
    final_df = pd.concat([df.reset_index(drop=True), structured_df.reset_index(drop=True)], axis=1) # Merge extracted data with original dataset
    save_data(final_df, output_csv, output_json, output_jsonl)

if __name__ == "__main__":
    main()
