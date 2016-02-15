
import smtplib
import time
from email.mime.text import MIMEText  

mail_host="smtp.126.com"  #设置服务器
mail_user="manyadaibao"    #用户名
mail_pass="59421ting"   #口令 
mail_postfix="126.com"  #发件箱的后缀
   
def send_mail(sub,content):  
    to_list=["58254451@qq.com"]
    me="<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    print(msg.as_string())
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception as e:  
        print (str(e))  
        return False  

def run(logname,title):

    file=open(logname)
    t=file.readlines()
    if len(t)>0:
        send_mail(title,"".join(t))

    file.close()
    file=open(logname,"w")
    file.write('')
    file.close()

if __name__ == '__main__':
    send_mail("测试下邮箱","".join("13122212112112"))