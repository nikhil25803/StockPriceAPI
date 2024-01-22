# StockPriceAPI

API for an application to access and manage data from the Bombay Stock Exchange (BSE). Based on the data released by Equity Bhavcopy [Link](https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx)

### Project Structure

```md
StockPriceAPI
├── 📄 LICENSE
├── 📄 README.md
├── 📄 .gitignore
├── 📄 .env
├── 📄 .requirements.txt
├── 📄 .dev-requirements.txt
└── 📂 api/
│ └──── 📂 db/
│ └──── 📂 models/
│ └──── 📂 routes/
│ └──── 📄 main.py
└── 📂 preprocessing/
│ └──── 📂 scrape_up/
│ │ ├──── 📄 script.py
```

### Project Setup

- Clone the repository

```bash
git clone https://github.com/nikhil25803/StockPriceAPI
```

```bash
cd StockPriceAPI
```

- Virtual Environment Setup

```bash
python -m venv env
```

- Download Requirements

```bash
pip install -r dev-requirements.txt
```

- Environment Variables Requirements

```.env
MONGO_URI=...
```

### Data Preprocessing

- Extract and read the CSV file in the ZIP.
- Store the data in MongoDB.
- Script with command line argument to extract and load stock data of any date.
- Added support to fetch the last 50 days' data.

#### Run script to extract and load stock data.

```bash
python preprocessing/script.py --help
```

Response:

```bash
usage: script.py [-h] [--date DATE] [--last50Days LAST50DAYS]

Download and load Bombay Stock Exchange data in the database

options:
  -h, --help            show this help message and exit
  --date DATE           Download Equity Bhavcopy data of a particular date Format: dd-mm-yyy. Eg. 09/01/2024
  --last50Days LAST50DAYS
                        Load the last 50 days' data.
```

Example: Load data of date 20/01/2023

```bash
python preprocessing/script.py --date 20/01/2023
```

This will download Equity Bhavcopy data and load it into the MongoDB database.

### API

Start the server:

```bash
uvicorn api.main:app --reload
```

> You can listen to the server on `http://127.0.0.1:8000/`

Access the endpoints through UI by OpenAPI on `/docs` path.

#### Endpoint Summary

- A GET route for the top 10 stocks.
- A GET route to find stocks by name.
- A GET router to get a stock price history list for the UI graph.
- A POST route to add a stock to favorites.
- A GET route to see favorite stocks.
- A DELETE route to remove a stock from favorites
