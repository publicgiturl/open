CREATE TABLE MERGE
AS SELECT C.company, D.code, D.date, D.open, D.high, D.low, D.close, D.diff, D.volume
FROM company_info C
JOIN daily_price D
ON C.code = D.code;