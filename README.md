# Project Title

A small project I worked on: Data analysis on reddit r/sportsbook POTD. Data collection by scraping Reddit's r/sportbook (praw) and gathered the top 10 daily comments from the POTD flair.

To ensure clean and consistent data, I used LLM namely Mistral:7b to parse and refine the text.
- Note: There may be errors given limitations of the LLM

Disclaimer: This project does not promote or endorse gambling. If you choose to gamble, please do so responsibly.

---

## Overview

This repository contains scripts, notebooks, and data related to analyzing “Pick of the Day” (POTD) entries for the years 2024. It includes data extraction from links, cleaning for large language model (LLM) processing, and outcome analysis. The goal is to see the relationship if any between the POTD and user engagement 

---

## Project Structure

Below is a high-level overview of the folders and files in this repository.
(Note: Certain items may not be publicly available, either for confidentiality or relevance reasons.)

### Folders

#### `data/`
- **2024_llm_POTD_identified_clean.csv**  
  A CSV file containing POTD data for 2024 that has been processed to identify certain fields suitable for LLM input.

- **2024_POTD_cleaned.csv**  
  A cleaned CSV of the 2024 POTD data. May include standardized columns, filtered rows, or normalized text.

- **2024_POTD_top10each.csv**  
  A CSV filtered down to the top 10 POTD entries.

- **2024_result_with_search.csv**  
  A CSV showing result rows combined with additional information from search operations.

- **2024_result.csv**  
  A final results CSV for 2024 POTD.

#### `links/`
- **2024_Post_Links.csv**  
  A CSV containing links (URLs) for posts in 2024. Could be used by `POTDfromLink.py` or other scripts to fetch or parse data.


### Top-Level Files

- **Analysis.ipynb**  
  Jupyter notebook that performs exploratory analysis on the POTD data. Include visualizations and statistical checks.

- **clean_for_LLM.py**  
  Python script that further cleans and standardizes text data to be suitable for large language model (LLM) inputs. Includes tokenization, removing special characters, or handling null entries.

- **config.py**  
  Python file containing configuration values such as file paths, API keys, or constants used across multiple scripts.

- **extract_pick_mistral.py**  
  Python script specifically related to the “Mistral:7b” LLM workflow.

- **llm_clean.py**  
  Another cleaning utility script focusing on data preparation for any LLM pipeline.

- **outcome_result_mistral.py**  
  Python script that interprets the final outcomes from the Mistral LLM runs.

- **POTDfromLink.py**  
  Python script that extracts "Pick of the Day” entries from the links provided in CSVs `2024_Post_Links.csv` and `2025_Post_Links.csv`). 

- **test.ipynb**  
  notebook to test and visualize results

- **README.md**  
  This file, providing an overview of the project, its structure, and instructions.

---
