INSERT INTO stock_back
SELECT * FROM stock_back WHERE CONCAT(stockid,DATE,TIME) NOT IN 
(SELECT CONCAT(stockid,DATE,TIME) FROM (SELECT * FROM `stock` WHERE  STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')<DATE_ADD(NOW(),INTERVAL -5 DAY) ) a 
)

/*备份当前表的历史数据到back表*/

DELETE FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')<DATE_ADD(NOW(),INTERVAL -5 DAY)
/*删除当前表5天前的历史数据*/


SELECT * FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')>DATE_ADD(NOW(),INTERVAL -5 DAY)

