# Database Changelog


# Version 1.0.0


## Table: trades


Stores Binance trade information.


| Column | Type | Description |
|-|-|-|
| id | INTEGER | Binance trade ID |
| symbol | STRING | BTCUSDT |
| side | STRING | BUY / SELL |
| price | DOUBLE | Trade price |
| quantity | DOUBLE | BTC amount |
| profit_loss | DOUBLE | Profit |
| roi | DOUBLE | ROI % |
| created_at | TIMESTAMP | Date |


---

## Example


```json
{
"id":12345,
"symbol":"BTCUSDT",
"side":"BUY",
"price":67420.50,
"quantity":0.01,
"profit_loss":50,
"roi":2.4
}
```