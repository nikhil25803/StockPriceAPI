from pydantic import BaseModel
from typing import List


class Stock(BaseModel):
    """Model for Stocks response"""

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
    """Model for stock history"""

    OPEN: float
    HIGH: float
    LOW: float
    CLOSE: float
    date: str


class TopStocksResponse(BaseModel):
    """Model for list of Stocks"""

    data: List[Stock]
    message: str


class StockDataResponse(BaseModel):
    """Model for single stock response"""

    data: List[Stock] | None = None
    message: str
    status: int


class StockHistoryResponse(BaseModel):
    """Model list of stock hostiry"""

    data: List[StockHistory] | None = None
    message: str
    status: int
