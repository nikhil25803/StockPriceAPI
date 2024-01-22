"""
Imports
"""
import pandas
import requests, argparse, re, os
from io import BytesIO
from zipfile import ZipFile
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Take environment variables from .env.
load_dotenv()


def load_data_to_database(filename: str, file_date: str) -> bool:
    """Function load CSVC"""

    # Get the Mongo DB URL from .env file
    MONGO_URI = os.environ.get("MONGO_URI")

    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi("1"))

    # Test the connection
    try:
        client.admin.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print("Unable to connect to DB.\nError: ", e)
        return False

    # accessing the database
    database = client["BSEData"]

    # access collection of the database
    collection = database["stock-price"]

    # File path
    file_path = os.path.join(os.getcwd(), "data", f"{filename.split('_')[0]}.CSV")

    # Read the CSV File
    data = pandas.read_csv(file_path)

    # Add a new columns - date
    data["date"] = file_date

    # Strip the whitespace around name
    data["SC_NAME"] = data["SC_NAME"].str.strip()

    # Convert each data into a dict and store them in a list
    data_list = [data.iloc[i, :].to_dict() for i in range(len(data))]

    # Add this list to mongo DB database
    try:
        collection.insert_many(data_list)
    except Exception as e:
        print("Unable to add records in database\nError: ", e)

    return True


def download_csv_data(date: str) -> bool:
    """Function to download CSV data"""

    # Formatting file name from date
    day = date.split("/")[0]
    month = date.split("/")[1]
    year = date.split("/")[2][2:]

    file_name_from_date = f"EQ{day}{month}{year}_CSV.ZIP"

    # Defining file URL
    file_url = (
        f"https://www.bseindia.com/download/BhavCopy/Equity/{file_name_from_date}"
    )

    # Headers
    headersList = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    }

    target_directory = os.path.join(os.getcwd(), "data")

    try:
        url_response = requests.request("GET", file_url, headers=headersList)

        # Load the Zip file and extract the content
        with ZipFile(BytesIO(url_response.content)) as zip_file:
            zip_file.extractall(target_directory)

        # Try to load the data into the database
        db_response = load_data_to_database(
            filename=file_name_from_date, file_date=f"{day}/{month}/{year}"
        )

        if db_response == False:
            return False

    except Exception as e:
        print("Unable to process.\nError: ", e)
        return False

    return True


# Main function accepting Command Line Arguments
if __name__ == "__main__":
    # An argument parser object
    parser = argparse.ArgumentParser(
        description="Download and load Bombay Stock Exchange data in the database"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="Download Equity Bhavcopy data of a particular date\nFormat: dd-mm-yyy. Eg. 09/01/2024",
        required=False,
    )
    parser.add_argument(
        "--last50Days", type=bool, help="Load last 50 days data.", required=False
    )

    # Variable to listed arguments
    args = parser.parse_args()

    # If last 50 days data is requested
    if args.last50Days == True:
        pass
    elif args.date:
        # Entered date
        date_string = args.date

        # Regex to validate date
        date_pattern = re.compile(r"\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}\b")

        # Check if entered date is matched or not
        if date_pattern.match(date_string):
            # Download the file
            response = download_csv_data(date=date_string)

            if response == False:
                print("Unable to download and load the data")
        else:
            print(f"{date_string} is not a valid date in the dd/mm/yyyy format.")
    else:
        print(
            "Please provide values to either --date or --last50Days arguments.\nOr enter --help."
        )
