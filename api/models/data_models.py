from pydantic import BaseModel
from typing import List


class Stock(BaseModel):
    """Stock Data Model"""

    SC_CODE: float
    SC_NAME: str
    SC_GROUP: str
    SC_TYPE: str
    OPEN: float
    HIGH: float
    LOW: float
    CLOSE: float
    LAST: float
    PREVCLOSE: float
    NO_TRADES: float
    NO_OF_SHRS: float
    NET_TURNOV: float
    date: str


class StockHistory(BaseModel):
    """Stock History Data Model"""

    OPEN: float
    HIGH: float
    LOW: float
    CLOSE: float
    date: str


class FavouriteStock(BaseModel):
    """Favourite Stock Data Model"""

    SC_CODE: str


class TopStocksResponse(BaseModel):
    """Top Stock Data Response"""

    data: List[Stock]
    message: str


class StockDataResponse(BaseModel):
    """Stock Data Response"""

    data: List[Stock] | None = None
    message: str
    status: int


class StockHistoryResponse(BaseModel):
    """Stock Data History Response"""

    data: List[StockHistory] | None = None
    message: str
    status: int


class FavouriteStockResponse(BaseModel):
    """Favourite Stock Data Reponse"""

    data: List[FavouriteStock] | None = None
    message: str
    status: int
