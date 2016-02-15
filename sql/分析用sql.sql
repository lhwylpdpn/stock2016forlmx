
SHOW STATUS;
SELECT a.stockid,a.date,a.time,a.close,b.stockid,b.date,b.time,b.close FROM (
(SELECT * FROM `stock` WHERE stockid='audchf') a ,

(SELECT * FROM `stock` WHERE stockid='nzdchf') b )
WHERE a.date=b.date AND a.time=b.time AND  STR_TO_DATE(CONCAT(a.DATE,' ',a.TIME),'%Y.%c.%d %H:%i')>=DATE_ADD(NOW(),INTERVAL -11116 DAY) ORDER BY STR_TO_DATE(CONCAT(a.DATE,' ',a.TIME),'%Y.%c.%d %H:%i')


SELECT stockid,COUNT(*) FROM stock_back GROUP BY stockid

SELECT stockid FROM stock_foreign.stock_back WHERE stockid IN ('NZDCHF15.csv','AUDCHF15.csv','AUDNZD15.csv','EURAUD15.csv') GROUP BY stockid;


SELECT *,LN(openb)-LN(opena)-ln_e_open ,ln_e_close-(LN(openb)-LN(opena)), ((closeA-openA)*lots_A+(openB-closeB)*lots_B)/(openA*lots_A+openB*lots_B),LN(openb)-LN(opena),LN(closeB)-LN(closeA) FROM order_result WHERE ((closeA-openA)*lots_A+(openB-closeB)*lots_B)/(openA*lots_A+openB*lots_B)>0



SELECT * ,LN(openb)-LN(opena)-ln_e_close,((closeA-openA)*lots_A+(openB-closeB)*lots_B)/(openA*lots_A+openB*lots_B) AS 盈利率 FROM `order_result` WHERE LN(openb)-LN(opena)-ln_e_close<0
/*查看建仓正确性有问题的订单*/


SELECT (b.openb-b.opena+a.c)/(b.opena+b.openb),b.* FROM `order_result` b ,(
SELECT MIN(a.low-b.high) AS c,a.stockid AS s1,b.stockid AS s2 FROM stock_back_allshuju a , stock_back_allshuju b 
 WHERE a.stockid='USDCHF' AND b.stockid='AUDSGD' AND a.date=b.date AND a.time=b.time) a WHERE a.s1=b.namea AND a.s2=b.nameb


SELECT *,(a.openb-a.opena+b.huiche)/(a.opena+a.openb) FROM `order_result` a LEFT JOIN 
(SELECT a.stockid AS namea,b.stockid AS nameb,MIN(a.low-b.high) AS huiche FROM stock_back_allshuju a ,stock_back_allshuju b WHERE a.date=b.date AND a.time=b.time AND a.stockid<>b.stockid GROUP BY 
a.stockid,b.stockid) b ON a.namea=b.namea AND a.nameb=b.nameb AND a.


SELECT a.*,STR_TO_DATE(CONCAT(b.DATE,' ',b.TIME),'%Y.%c.%d %H:%i') FROM `order_result` a ,stock_back_allshuju b ,stock_back_allshuju c WHERE a.namea=b.stockid AND a.nameb=c.stockid AND b.date=c.date AND b.time=c.time
AND b.stockid<>c.stockid AND openA_time<STR_TO_DATE(CONCAT(b.DATE,' ',b.TIME),'%Y.%c.%d %H:%i') AND closeA_time>STR_TO_DATE(CONCAT(b.DATE,' ',b.TIME),'%Y.%c.%d %H:%i')





