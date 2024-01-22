import pymongo
from ..db.db_config import client
from fastapi import APIRouter, status, HTTPException
from ..models.data_models import (
    TopStocksResponse,
    StockDataResponse,
    StockHistoryResponse,
)
from bson import json_util
import json

# API Route
router = APIRouter(prefix="/api", tags=["API"])


@router.get(
    "/top-stocks", description="Get top 10 stocks", response_model=TopStocksResponse
)
async def top_stocks():
    """A GET route for the top 10 stocks."""

    # Defining collection name
    db = client["BSEData"]
    collection = db["stock-price"]

    try:
        # Fetch the sorted value of stocks data in Descending order
        results = collection.aggregate(
            pipeline=[{"$sort": {"CLOSE": pymongo.DESCENDING}}]
        )

        # Response
        return {
            "data": list(results)[:10],
            "message": "Top 10 stocks data has been fetched (sorted by CLOSED value)",
            "status": status.HTTP_200_OK,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to fetch records.\nError: {e}",
        )


@router.get(
    "/stock/{name}",
    description="Find stocks by name",
    response_model=StockDataResponse,
)
async def stock_by_name(name: str):
    """A GET route to find stocks by name"""

    # Defining collection name
    db = client["BSEData"]
    collection = db["stock-price"]

    try:
        # Use $match in the aggregation pipeline to filter by SC_NAME
        results = collection.aggregate(pipeline=[{"$match": {"SC_NAME": name}}])

        # Convert the cursor to a list to evaluate its length
        results_list = list(results)

        # Check if any results were found
        if len(results_list) == 0:
            return {
                "data": [],
                "message": f"No stock data available for: {name}",
                "status": status.HTTP_404_NOT_FOUND,
            }
        else:
            # Return only the first document if there are multiple matches
            return {
                "data": results_list,
                "message": f"Fetched stock data of name: {name}",
                "status": status.HTTP_200_OK,
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to fetch record of given stock.\nError: {e}",
        )


@router.get(
    "/stock/history/{name}",
    description="Get stock price history list for UI graph",
    response_model=StockHistoryResponse,
)
async def stock_by_name(name: str):
    """A GET route to find stocks by name"""

    # Defining collection name
    db = client["BSEData"]
    collection = db["stock-price"]

    try:
        # Use $match in the aggregation pipeline to filter by SC_NAME
        results = collection.aggregate(pipeline=[{"$match": {"SC_NAME": name}}])

        # Convert the cursor to a list to evaluate its length
        results_list = list(results)

        # Check if any results were found
        if len(results_list) == 0:
            return {
                "data": [],
                "message": f"No hisptry available for stock: {name}",
                "status": status.HTTP_404_NOT_FOUND,
            }
        else:
            # Return only the first document if there are multiple matches
            return {
                "data": results_list,
                "message": f"Fetched history of stock: {name}",
                "status": status.HTTP_200_OK,
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to fetch data of given stock.\nError: {e}",
        )
