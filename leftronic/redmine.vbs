'mysql连接代码
strconnection = "dsn=10.1.11.63;driver={myodbd driver};server=10.1.11.63;uid=mysqladmin;pwd=123465; database=showdb" '数据库名为ly
'strconnection="DefaultDir=;driver={myodbd driver};database=ly" 　'这种不用DSN的方法我没有成功

Set adoDataConn = CreateObject("ADODB.Connection") 
adoDataConn.Open strConnection

	DB_PV_all = "SELECT COUNT(*) AS result FROM sys_log WHERE event='login' AND username NOT IN ('wangzhipeng','zhangchengtao','liuhao_17173','yuecui','liutiesong')" 
	Set rs = adoDataConn.Execute(DB_PV_all) 

		If Not rs.BOF Then
		Do While Not rs.EOF
		DB_PV_all=rs("result")
		rs.MoveNext 
		Loop
		Else 
		wscript.echo "Sorry, no data found."
		End If
	rs.Close 

		DB_PV = "SELECT  CONCAT(a/b*100,'%') AS a , description FROM (SELECT COUNT(*) AS a,(SELECT COUNT(*) FROM sys_log WHERE event='click' AND username NOT IN ('wangzhipeng','zhangchengtao','liuhao_17173','yuecui','liutiesong')) AS b,description  FROM sys_log WHERE event='click' AND username NOT IN ('wangzhipeng','zhangchengtao','liuhao_17173','yuecui','liutiesong') GROUP BY description) a" 
	Set rs = adoDataConn.Execute(DB_PV) 

		If Not rs.BOF Then
		Do While Not rs.EOF
		
		rs.MoveNext 
		Loop
		Else 
		wscript.echo "Sorry, no data found."
		End If
	rs.Close 

DB_PV_r="[{\"+Chr(34)+"name\"+Chr(34)+":\"+Chr(34)+"Cheryl\"+Chr(34)+","+Chr(34)+"value\"+Chr(34)+":111}]"

adoDataConn.Close 
Set adoDataConn = Nothing
createobject("wscript.shell").run "redmine.bat "&DB_PV_r