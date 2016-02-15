
SELECT *,CONCAT(ROUND((成功率*平均成功盈利率+失败率*平均失败盈利率)/100,5),"%") AS 数学期望 ,
CONCAT(ROUND((成功率*平均成功盈利率+失败率*平均失败盈利率)/100*日均开单 ,5),"%") AS "预期日化收益 " FROM (
SELECT CONCAT(ROUND(SUM(CASE WHEN a>0 THEN 1 END) /COUNT(*)*100,2),"%") AS 开仓正确率 ,
CONCAT(ROUND(SUM(CASE WHEN c>0 THEN 1 END) /COUNT(*)*100,2),"%") AS 成功率,
CONCAT(ROUND(AVG(CASE WHEN c>0 THEN c/openA END )*100,4),"%") AS 平均成功盈利率,
(AVG(CASE WHEN c>0 THEN TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) END )) AS 平均成功持仓时间,
(AVG(CASE WHEN c<0 THEN TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) END )) AS 平均失败持仓时间,
CONCAT(ROUND(SUM(CASE WHEN c<0 THEN 1 END) /COUNT(*)*100,2),"%") AS 失败率,
CONCAT(ROUND(AVG(CASE WHEN c<0 THEN c/openA END )*100,4),"%") AS 平均失败盈利率,
COUNT(*)/TIMESTAMPDIFF(DAY,openA_time,NOW()) AS 日均开单

 FROM (SELECT CASE WHEN order_type=0 THEN a.price_close_except-b.openA  WHEN   order_type=1 THEN b.openA-a.price_close_except END AS a,
 CASE WHEN order_type=0 THEN b.closeA-b.openA  WHEN   order_type=1 THEN b.openA-b.closeA END AS c,b.openA,b.openA_time,b.closeA_time

FROM `order` a,`order_result` b WHERE a.orderid=b.orderid  AND b.lots_A=0.01) b /*开仓正确性,陈功率*/) b
UNION
SELECT '平均失败盈利率','失败补仓总单数','最大补仓数','平均补仓持仓时间','平均日盈利比例','-','-','-','-','-'
UNION
SELECT 平均失败盈利率,失败补仓总单数,最大补仓数,平均补仓持仓时间,
CONCAT(平均失败盈利率*失败补仓总单数/(STR_TO_DATE(DATE_FORMAT(MIN(NOW()),'%y.%m.%d'),'%Y.%c.%d ') -STR_TO_DATE(DATE_FORMAT(MIN(openA_time),'%y.%m.%d'),'%Y.%c.%d ')+1),"%") AS 平均日盈利比例,'-','-','-','-','-' FROM (
SELECT
CONCAT(ROUND(AVG(CASE WHEN c>0 THEN c/openA END )*100,4),"%") AS 平均失败盈利率,
COUNT(*) AS 失败补仓总单数,
MAX(lots_A) AS 最大补仓数,
TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) AS 平均补仓持仓时间,openA_time,closeA_time
 FROM ( SELECT 
 CASE WHEN order_type=0 THEN closeA-openA  WHEN   order_type=1 THEN openA-closeA END AS c,openA,lots_A,openA_time,closeA_time


FROM `order_result` WHERE lots_A<>0.01) b /*开仓正确性,陈功率*/) a ;

/*//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////v*/
SELECT *,CONCAT(ROUND((成功率*平均成功盈利率+失败率*平均失败盈利率)/100,5),"%") AS 数学期望 ,
CONCAT(ROUND((成功率*平均成功盈利率+失败率*平均失败盈利率)/100*日均开单 ,5),"%") AS "预期日化收益 " FROM (
SELECT STR_TO_DATE(b.openA_time,'%Y.%c.%d') AS 日期, CONCAT(ROUND(SUM(CASE WHEN a>0 THEN 1 END) /COUNT(*)*100,2),"%") AS 开仓正确率 ,
CONCAT(ROUND(SUM(CASE WHEN c>0 THEN 1 END) /COUNT(*)*100,2),"%") AS 成功率,
CONCAT(ROUND(AVG(CASE WHEN c>0 THEN c/openA END )*100,4),"%") AS 平均成功盈利率,
(AVG(CASE WHEN c>0 THEN TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) END )) AS 平均成功持仓时间,
(AVG(CASE WHEN c<0 THEN TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) END )) AS 平均失败持仓时间,
CONCAT(ROUND(SUM(CASE WHEN c<0 THEN 1 END) /COUNT(*)*100,2),"%") AS 失败率,
CONCAT(ROUND(AVG(CASE WHEN c<0 THEN c/openA END )*100,4),"%") AS 平均失败盈利率,
COUNT(*) AS 日均开单

 FROM (SELECT CASE WHEN order_type=0 THEN a.price_close_except-b.openA  WHEN   order_type=1 THEN b.openA-a.price_close_except END AS a,
 CASE WHEN order_type=0 THEN b.closeA-b.openA  WHEN   order_type=1 THEN b.openA-b.closeA END AS c,b.openA,b.openA_time,b.closeA_time

FROM `order` a,`order_result` b WHERE a.orderid=b.orderid  AND b.lots_A=0.01) b GROUP BY  STR_TO_DATE(b.openA_time,'%Y.%c.%d')/*开仓正确性,陈功率*/) b 

UNION
SELECT '日期','平均失败盈利率','失败补仓总单数','最大补仓数','平均补仓持仓时间','平均日盈利比例','-','-','-','-' ,'-' 
UNION

SELECT 日期,平均失败盈利率,失败补仓总单数,最大补仓数,平均补仓持仓时间,
CONCAT(平均失败盈利率*失败补仓总单数,"%") AS 平均日盈利比例,
'-','-','-','-','-'   FROM (
SELECT
STR_TO_DATE(b.openA_time,'%Y.%c.%d') AS 日期,
CONCAT(ROUND(AVG(CASE WHEN c>0 THEN c/openA END )*100,4),"%") AS 平均失败盈利率,
COUNT(*) AS 失败补仓总单数,
MAX(lots_A) AS 最大补仓数,
TIMESTAMPDIFF(MINUTE,openA_time,closeA_time) AS 平均补仓持仓时间,openA_time,closeA_time
 FROM ( SELECT 
 CASE WHEN order_type=0 THEN closeA-openA  WHEN   order_type=1 THEN openA-closeA END AS c,openA,lots_A,openA_time,closeA_time


FROM `order_result` WHERE lots_A<>0.01) b GROUP BY  STR_TO_DATE(b.openA_time,'%Y.%c.%d') /*开仓正确性,陈功率*/) a 