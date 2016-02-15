SELECT a.stockid,a.date,a.time,a.close,b.stockid,b.date,b.time,b.close FROM (
(SELECT * FROM `stock_back` WHERE stockid='EURCAD') a ,

(SELECT * FROM `stock_back` WHERE stockid='EURSGD') b )
WHERE a.date=b.date AND a.time=b.time ORDER BY STR_TO_DATE(CONCAT(a.DATE,' ',a.TIME),'%Y.%c.%d %H:%i')