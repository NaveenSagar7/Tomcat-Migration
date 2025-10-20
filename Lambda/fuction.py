import json
import boto3
import pymysql

# Database configuration
db_config = {
    "host": "database-1-instance-1.c7uq2skoqqmb.ap-south-1.rds.amazonaws.com",       # Replace with your DB cluster endpoint (writer)
    "user": "Admin",                          # Replace with your DB username
    "password": "Naveensagar30",              # Replace with your DB password
    "database": "realmadrid_db"
}

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            key = record['s3']['object']['key']  # e.g., players/benzema.jpg

            # Skip if it's not under the 'players/' folder
            if not key.startswith("players/"):
                continue

            # Extract file name from path: players/benzema.jpg → benzema.jpg
            filename = key.split('/')[-1]

            # Extract player name from filename: benzema.jpg → Benzema
            player_name = filename.split('.')[0].replace('-', ' ').title()

            # Insert into DB
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                query = "INSERT INTO players (player_name, image_file) VALUES (%s, %s)"
                cursor.execute(query, (player_name, filename))
                connection.commit()

            print(f"Inserted {player_name} ({filename}) into DB.")

        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed')
        }
