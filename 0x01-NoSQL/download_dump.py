import gdown

# Replace the URL with the Google Drive link to your file.
file_url = 'https://drive.google.com/uc?id=1x9_DdyDb7kQ0dnwX1jMrROV3gqoz9wfR'

# Download the file from Google Drive.
gdown.download(file_url, quiet=False)

