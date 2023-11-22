import os
import psycopg2

# Database connection URI - replace with your actual URI
db_uri = "postgres://wpsgselj:t-RNQB1QDqyVGPLSNH54ONN93oU2rmiD@flora.db.elephantsql.com/wpsgselj"

# Directory containing TXT files
directory = "/home/marcel/PycharmProjects/pythonProject/postings"

# Connect to your PostgreSQL database using the URI
conn = psycopg2.connect(db_uri)
cur = conn.cursor()


# Function to process each file
def process_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

        # Extracting details from the file
        title, description, industry, address, visa_required, \
            datetime_posted, seniority, salary = lines[:8]

        # SQL query to insert data
        cur.execute("""
        INSERT INTO jobs (title, description, industry, address, provides_visa, post_time, seniority, salary)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
                    (title, description, industry, address,
                     bool(int(visa_required)), datetime_posted, int(seniority),
                     int(salary)))

        print("Imported file " + file_path)


# Process each TXT file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        process_file(os.path.join(directory, filename))

# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()
