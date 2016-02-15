TRUNCATE TABLE `stock`;
TRUNCATE TABLE `releation_mid`;


DROP TABLE bushuju;
CREATE TABLE bushuju 
SELECT * FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') IN (SELECT  STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') FROM stock GROUP BY stockid,STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') HAVING COUNT(*)<>1

) AND stockid IN (SELECT stockid FROM stock GROUP BY stockid,STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') HAVING COUNT(*)<>1
) GROUP BY stockid,STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') ;

DELETE FROM stock WHERE stockid IN (SELECT stockid FROM  bushuju) AND STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') IN (SELECT STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i') FROM bushuju);

INSERT INTO stock SELECT * FROM bushuju;
/*慎重用，删除掉数据中 重复的项，会有小影响*/



SELECT * FROM stock WHERE STR_TO_DATE(CONCAT(DATE,' ',TIME),'%Y.%c.%d %H:%i')<=DATE_ADD(NOW(),INTERVAL -5 DAY)

SELECT a.stockidA, a.stockidB ,a.releation ,a.lnA_B,a.avgA_B,a.stdA_B,b.`releation` FROM releation_mid a, releation_mid_prev b WHERE a.`stockidA`=b.`stockidA` AND a.`stockidB`=b.`stockidB` 


SELECT DISTINCT a.date,a.time,a.close,b.close FROM stock a ,stock b WHERE a.stockid='CADCHF' AND b.stockid='AUDCAD' AND a.date=b.date AND a.time=b.time ORDER BY  STR_TO_DATE(CONCAT(a.date,' ',a.TIME),'%Y.%c.%d %H:%i') DESC LIMIT 102