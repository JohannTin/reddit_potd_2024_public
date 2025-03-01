# Project Title

A small project I worked on: Data analysis on reddit r/sportsbook POTD. Data collection by scraping Reddit's r/sportbook (praw) and gathered the top 10 daily comments from the POTD flair.

To ensure clean and consistent data, I used LLM namely Mistral:7b to parse and refine the text.
- Note: There may be errors given limitations of the LLM

---

## Overview

This repository contains scripts, notebooks, and data related to analyzing “Post of the Day” (POTD) entries for the years 2024. It includes data extraction from links, cleaning for large language model (LLM) processing, and outcome analysis. The goal is to demonstrate how to handle text data across multiple steps, from raw links to final results.

---

## Project Structure

Below is a breakdown of the key folders and files you’ll find in this repository:

### Folders

#### `data/`
- **2024_llm_POTD_identified_clean.csv**  
  A CSV file containing POTD data for 2024 that has been processed to identify certain fields suitable for LLM input. Data is “clean” in the sense that extraneous information or noise has been removed.

- **2024_POTD_cleaned.csv**  
  A cleaned CSV of the 2024 “Post of the Day” data. May include standardized columns, filtered rows, or normalized text.

- **2024_POTD_top10each.csv**  
  A CSV filtered down to the top 10 POTD entries for each category/day/month (depending on your logic). Useful for quick analyses or examples.

- **2024_result_with_search.csv**  
  A CSV showing result rows combined with additional information from search operations (e.g., if you performed web lookups or extended context queries).

- **2024_result.csv**  
  A final or intermediate results CSV for 2024 POTD. Often used in conjunction with the “with_search” version.

#### `links/`
- **2024_Post_Links.csv**  
  A CSV containing links (URLs) for posts in 2024. Could be used by `POTDfromLink.py` or other scripts to fetch or parse data.


### Top-Level Files

- **Analysis.ipynb**  
  A Jupyter notebook that performs exploratory or in-depth analysis on the POTD data. May include visualizations, statistical checks, or demonstration of the cleaning pipeline.

- **clean_for_LLM.py**  
  A Python script that further cleans or standardizes text data to be suitable for large language model (LLM) inputs. It might include tokenization, removing special characters, or handling null entries.

- **config.py**  
  A Python file containing configuration values such as file paths, API keys, or constants used across multiple scripts.

- **extract_pick_mistral.py**  
  A Python script specifically related to the “Mistral:7b” LLM workflow.

- **llm_clean.py**  
  Another cleaning utility script focusing on data preparation for any LLM pipeline.

- **outcome_result_mistral.py**  
  A Python script that interprets the final outcomes from the Mistral LLM runs.

- **POTDfromLink.py**  
  A Python script that extracts "Pick of the Day” entries from the links provided in CSVs `2024_Post_Links.csv` and `2025_Post_Links.csv`). 

- **test.ipynb**  
  A notebook to test and visualize results

- **README.md**  
  This file, providing an overview of the project, its structure, and instructions.

---

## Installation & Requirements

1. **Clone the repository**:
   ```bash
   git clone https://github.com/username/repo-name.git
   cd repo-name
