import pandas as pd
import re

"""
Extracts only numerical values from the "Odds" column.
Converts American odds to decimal (if necessary).
If "Odds" is missing or outside -200 to +200 (or 1.5 to 3.0), sets it to 1.86.
Extracts and cleans "Unit" values, ensuring they are between 1 and 5.
If "Unit" is missing or outside range, defaults to 1.
Drops rows where "Pick" is missing or "N/A".
"""

def load_csv(file_path):
    """Loads the CSV file into a DataFrame."""
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def filter_columns(df, start_col, end_col):
    """Filters the DataFrame to include only columns from start_col to end_col."""
    try:
        filtered_df = df.loc[:, start_col:end_col]
        return filtered_df
    except KeyError:
        print("Error: One or more specified columns not found in the dataset.")
        return None

def clean_data(df):
    """Cleans the data: Drops rows where 'Pick' is NaN or 'N/A', extracts and validates odds and units."""
    
    # Drop rows where 'Pick' is NaN or 'N/A'
    if 'Pick' in df.columns:
        df = df.dropna(subset=['Pick']) 
        df = df[df['Pick'].str.strip().str.upper() != 'N/A']
    else:
        print("Warning: 'Pick' column not found in the dataset.")

    # Clean and validate "Odds" column
    if 'Odds' in df.columns:
        df['Odds'] = df['Odds'].apply(lambda x: extract_and_validate_odds(str(x)))
    else:
        print("Warning: 'Odds' column not found in the dataset. Assigning default odds.")
        df['Odds'] = 1.86  # Assign default odds if column is missing

    # Clean and validate "Unit" column
    if 'Unit' in df.columns:
        df['Unit'] = df['Unit'].apply(lambda x: extract_and_validate_unit(str(x)))
    else:
        print("Warning: 'Unit' column not found in the dataset. Assigning default unit.")
        df['Unit'] = 1  # Default unit if column is missing
    
    return df

def extract_and_validate_odds(odds_str):
    """Extracts numerical odds, converts American odds to decimal, and ensures it falls within valid range.
       If odds are missing or out of range, return default value 1.86."""
    odds_str = odds_str.strip()

    # Check if the odds are in American format (-200 to +200)
    if re.match(r"^-?\d+$", odds_str):  # If it's a pure integer (American odds)
        american_odds = int(odds_str)
        decimal_odds = convert_american_to_decimal(american_odds)
        if 1.5 <= decimal_odds <= 3.0:
            return decimal_odds
        else:
            return 1.86 

    # If already in decimal format, just return as float
    try:
        decimal_odds = float(odds_str)
        if 1.5 <= decimal_odds <= 3.0:
            return decimal_odds
        else:
            return 1.86  # Default if out of range
    except ValueError:
        return 1.86 

def convert_american_to_decimal(american_odds):
    """Converts American odds to decimal odds."""
    if american_odds > 0:
        return round((american_odds / 100) + 1, 2)
    elif american_odds < 0:
        return round((100 / abs(american_odds)) + 1, 2)
    else:
        return 1.86  # Default odds for invalid cases

def extract_and_validate_unit(unit_str):
    """Extracts only the numerical value from the 'Unit' column and ensures it is between 1 and 5.
       If no unit is found or out of range, returns default value 1."""
    match = re.search(r"\d+", unit_str)  # Extracts first numeric value
    if match:
        unit_value = int(match.group())
        return unit_value if 1 <= unit_value <= 5 else 1  # Ensure range 1-5, else default to 1
    return 1  # Default to 1 if no numeric value is found

def save_csv(df, output_file_path):
    """Saves the DataFrame to a new CSV file."""
    try:
        df.to_csv(output_file_path, index=False)
        print(f"File successfully saved as: {output_file_path}")
    except Exception as e:
        print(f"Error saving file: {e}")

def main():
    input_file_path = "data/llm_POTD_identified.csv"
    output_file_path = "data/2024_llm_POTD_identified_clean.csv"

    df = load_csv(input_file_path)
    if df is None:
        return

    filtered_df = filter_columns(df, 'Extracted_Date', 'Unit')
    if filtered_df is None:
        return

    cleaned_df = clean_data(filtered_df)

    save_csv(cleaned_df, output_file_path)

if __name__ == "__main__":
    main()
