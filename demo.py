import gdown
import os

# https://drive.google.com/file/d/152PyisZggi2W5xum38LNTHapCK59CI6Z/view?usp=sharing
# Create the folder if it doesn't exist
os.makedirs('data', exist_ok=True)

# File ID from Google Drive link
file_id = '152PyisZggi2W5xum38LNTHapCK59CI6Z'
url = f'https://drive.google.com/uc?id={file_id}'

# Specify the full path to save the file
output_path = 'encoded_df.pkl'

# Download file
gdown.download(url, output_path, quiet=False)

print(f"File downloaded to: {os.path.abspath(output_path)}")