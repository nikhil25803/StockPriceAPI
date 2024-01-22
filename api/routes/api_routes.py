import pymongo
from ..db.db_utils import (
    db_aggregation,
    db_delete,
    db_fetch_all,
    db_find_one,
    db_insert_one,
)
from fastapi import APIRouter, status, HTTPException, Depends
from ..models.data_models import (
    TopStocksResponse,
    StockDataResponse,
    StockHistoryResponse,
    FavouriteStockResponse,
)
from fastapi.responses import JSONResponse
from cachetools import TTLCache

# A cache instance
cache = TTLCache(maxsize=5000, ttl=300)

# API Route
router = APIRouter(prefix="/api", tags=["API"])

"""A GET route for the top 10 stocks."""


@router.get(
    "/top-stocks", description="Get top 10 stocks", response_model=TopStocksResponse
)
async def top_stocks(cache: dict = Depends(lambda: cache)):
    # Returns the cached data if available
    if "top_stocks" in cache:
        return cache["top_stocks"]

    try:
        aggregated_response = await db_aggregation(
            db_name="BSEData",
            collection_name="stock-price",
            pipeline=[{"$sort": {"CLOSE": pymongo.DESCENDING}}],
        )

        top_stocks_data = {
            "data": aggregated_response[:10],
            "message": "Top 10 stocks data has been fetched (sorted by CLOSED value)",
            "status": status.HTTP_200_OK,
        }

        # Caching the response
        cache["top_stocks"] = top_stocks_data

        return top_stocks_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to fetch records.\nError: {e}",
        )


"""A GET route to find stocks by name"""


@router.get(
    "/stock/{name}",
    description="Find stocks by name",
    response_model=StockDataResponse,
)
async def stock_by_name(name: str, cache: dict = Depends(lambda: cache)):
    # Check for cached data
    if name in cache:
        return cache[f"{name}"]

    try:
        # DB Query
        aggregated_response = await db_aggregation(
            db_name="BSEData",
            collection_name="stock-price",
            pipeline=[{"$match": {"SC_NAME": name}}],
        )

        # Check if any results were found
        if len(list(aggregated_response)) == 0:
            return {
                "data": [],
                "message": f"No stock data available for: {name}",
                "status": status.HTTP_404_NOT_FOUND,
            }
        else:
            stock_data = {
                "data": aggregated_response,
                "message": f"Fetched stock data of name: {name}",
                "status": status.HTTP_200_OK,
            }

            # Caching the result
            cache[f"{name}"] = stock_data

            return stock_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to fetch record of given stock.\nError: {e}",
        )


"""A GET router to get stock price history list for UI graph."""


@router.get(
    "/stock/history/{name}",
    description="Get stock price history list for UI graph",
    response_model=StockHistoryResponse,
)
async def stock_by_name(name: str, cache: dict = Depends(lambda: cache)):
    # Check for cached data
    if f"{name}-history" in cache:
        return cache[f"{name}-history"]

    try:
        # DB Query
        aggregated_response = await db_aggregation(
            db_name="BSEData",
            collection_name="stock-price",
            pipeline=[{"$match": {"SC_NAME": name}}],
        )

        # Check if any results were found
        if len(aggregated_response) == 0:
            return {
                "data": [],
                "message": f"No hisptry available for stock: {name}",
                "status": status.HTTP_404_NOT_FOUND,
            }
        else:
            stock_history_data = {
                "data": aggregated_response,
                "message": f"Fetched history of stock: {name}",
                "status": status.HTTP_200_OK,
            }

            cache[f"{name}-history"] = stock_history_data

            return stock_history_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to fetch data of given stock.\nError: {e}",
        )


"""
A POST route to add a stock to favourites.
"""


@router.post("favourites/", description="Add a stock to favourites")
async def add_to_favourites(stock_code: str):
    # DB Query
    fav_stock = await db_find_one(
        db_name="BSEData", collection_name="favourites", filter={"SC_CODE": stock_code}
    )

    if fav_stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The stock is already added to favourites",
        )

    # If not, add to the favourite list
    try:
        await db_insert_one(
            db_name="BSEData",
            collection_name="favourites",
            data={"SC_CODE": stock_code},
        )

        return JSONResponse(
            content="Stock has been added to favourites successfully.",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Unable to add stock to favourites\nError: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


"""
A GET route to see favourite stocks.
"""


@router.get(
    "favourites/",
    description="See favourite all stocks.",
    response_model=FavouriteStockResponse,
)
async def get_all_favourites(cache: dict = Depends(lambda: cache)):
    # DB Query
    fav_stock = await db_fetch_all(db_name="BSEData", collection_name="favourites")

    try:
        if fav_stock:
            fav_stock_data = {
                "data": fav_stock,
                "message": f"Fetched all the favourite stocks",
                "status": status.HTTP_200_OK,
            }

            # Caching the result
            cache["fav-stocks"] = fav_stock_data

            return fav_stock_data
        else:
            return {
                "data": [],
                "message": f"No fevourite stocks data found",
                "status": status.HTTP_200_OK,
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to fetch favourite stocks data.\nError: {e}",
        )


"""
A DELETE route to remove a stock from favourites.
"""


@router.delete("favourites", description="Remove a stock from favourites")
async def remove_favourite_stock(stock_code: str):
    # DB Query
    fav_stock = await db_find_one(
        db_name="BSEData", collection_name="favourites", filter={"SC_CODE": stock_code}
    )

    if not fav_stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The stock with given code exist",
        )

    # If not, add to the favourite list
    try:
        # DB Query
        await db_delete(
            db_name="BSEData",
            collection_name="favourites",
            filter={"SC_CODE": stock_code},
        )

        # Response
        return JSONResponse(
            content="Stock has been removed from favourites",
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        raise HTTPException(
            detail=f"Unable to remove stocks from favourite.\nError: {e}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
