import sqlite3
import os
import psycopg2
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

image_directory = os.getenv("IMAGE_DIRECTORY")
database_path = os.getenv("DB_LOCAL_PATH")

# List of image paths
image_paths = os.listdir(image_directory)

image_file_types = [
    '.jpg',
    '.png',
    '.svg'
]

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

for image in image_paths:
    file_extension = os.path.splitext(image)[1]

# Iterate over the image paths and insert into the database
    if file_extension in image_file_types:
        image_path_housing = f'{image_directory}\{image}'
        with open(image_path_housing, "rb") as image_file:
            image_data = image_file.read()

# checking database "name" column against the image being processed.
# If result(count)=0, it means the name is not already present in the database and the record is inserted.
        image_name = image
        
        cursor.execute(os.getenv("SQL_STATEMENT_SELECT_IMAGES"), (image_name,))
        result = cursor.fetchone()

        if result[0] == 0:            
            cursor.execute(os.getenv("SQL_STATEMENT_INSERT_IMAGES"), (image_data, image_name))

conn.commit()
conn.close()