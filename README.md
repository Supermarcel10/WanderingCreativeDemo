# Job Posting Importer

This Python script is designed to import job postings from text files into a PostgreSQL database.

## How it Works

The script works by iterating over each text file in a specified directory. Each file represents a job posting and contains the following information, each on a separate line:

1. Job title
2. Job description
3. Industry
4. Address
5. Visa requirement (1 if visa is provided, 0 otherwise)
6. Date and time the job was posted
7. Seniority level (represented as an integer)
8. Salary

The script reads these details from each file and inserts them into a `jobs` table in the database.

## Database Connection

The script connects to the PostgreSQL database using a connection URI. This URI should be replaced with the actual URI of your database.

## Running the Script

Ensure that the `directory` variable in the script points to the directory containing your job posting text files.

To run the script, simply execute
```bash
python3 main.py
```

## Dependencies

This script requires the `psycopg2` library for connecting to the PostgreSQL database. You can install it using pip:

```bash
pip install psycopg2
```