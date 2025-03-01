#pip install praw

import praw
import pandas as pd
import datetime
import csv
import re
from config import reddit

# Load the CSV file containing post links
csv_file = "links/2024_Post_Links.csv"
data = pd.read_csv(csv_file)

# Prepare list for CSV export
comment_data = []


# Process each post link
for index, row in data.iterrows():
    post_title = row["Post Title"]
    post_link = row["Post link"]

    # Fetch the submission (Reddit post) using the link
    submission = reddit.submission(url=post_link)

    # Extract post details
    post_date = datetime.datetime.fromtimestamp(submission.created_utc)
    print(f"Processing Post: {post_title} - {post_date.strftime('%Y-%m-%d %H:%M:%S')}")

    # Extract top comments (sorted by karma)
    comments = [comment for comment in submission.comments.list() if isinstance(comment, praw.models.Comment)]
    top_comments = sorted(comments, key=lambda c: c.score, reverse=True)[:10]  # Get top x comments

    print(f"Total Comments: {len(comments)} - Extracting Top {len(top_comments)}")
    total_replies = sum(len(comment.replies) for comment in comments if hasattr(comment, 'replies'))
    print(f"Total Comments including replies: {len(comments) + total_replies}")

    for comment in top_comments:
        comment_data.append([
            post_title,  # Post Title from the CSV
            post_date.strftime('%Y-%m-%d %H:%M:%S'),  # Post Date
            comment.author.name if comment.author else "Deleted",  # Comment Author
            comment.score,  # Comment Karma
            datetime.datetime.fromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),  # Comment Date
            comment.body  # Comment Text
        ])

# Define CSV file path for output
output_csv = "2024_POTD_top10each.csv"

# Write to CSV file
with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Post_Title", "Post_Date", "Comment_Author", "Comment_Karma", "Comment_Date", "Comment_Text"])
    writer.writerows(comment_data)

print(f"Extracted {len(comment_data)} comments and saved to {output_csv}.")


# # Load the CSV file
# df = pd.read_csv(output_csv)

# # Display the first 5 rows
# print(df.head(10))