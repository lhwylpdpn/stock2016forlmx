//+------------------------------------------------------------------+
//|                                                     test2015.mq4 |
//|                        Copyright 2015, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2015, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
string orderA[];
string orderB_A[];
string py_orderid[];
string lnA_B[];
string lnA_B_except[];
string send_number[];
string close_bucang[];
string filename_all;
int tt[]={1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4181};
int filename_balance;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- create timer
   EventSetTimer(3);
   //load_continue();
//---
      filename_all="balance.txt";
      filename_balance=FileOpen(filename_all,FILE_READ|FILE_WRITE|FILE_TXT);
      load_continue();
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();

  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   order_close();
   clac_stop();
   printf("tick 正常");
   if (FileIsExist("tick.csv") && (Minute()==0 || Minute()==1|| Minute()==10|| Minute()==15|| Minute()==20|| Minute()==25|| Minute()==30|| Minute()==35|| Minute()==40 || Minute()==45|| Minute()==50|| Minute()==55))
   { tickcheck();}
    
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {

   printf(!FileIsExist("price_record.csv"));
   printf(Minute());
   if (!FileIsExist("price_record.csv") && (Minute()==1 || Minute()==6|| Minute()==11|| Minute()==16|| Minute()==21|| Minute()==26|| Minute()==31|| Minute()==36|| Minute()==41 || Minute()==46|| Minute()==51|| Minute()==56))
   { get_data();}
   // get_data();
   if(is_null_file("create.txt")!=0)
  {Print("有建仓需求");
   read_API();
  }
  }
   

 
  int is_null_file(string filename)
  { int h=FileOpen(filename,FILE_READ|FILE_TXT);
    int size= FileSize(h);
    FileClose(h);
    return(size);
   }
 
//+------------------------------------------------------------------+

//+---获取历史未完成的订单数据
//+------------------------------------------------------------------+ 
 
 
 void load_continue()
  {
   string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];

      while(!FileIsEnding(filename_balance))
      {

         u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
         int k=StringSplit(FileReadString(filename_balance),u_sep,result);
   //--- Show a comment 

       ArrayResize(orderA,ArraySize(orderA)+1);
       ArrayResize(py_orderid,ArraySize(py_orderid)+1);
       ArrayResize(lnA_B,ArraySize(lnA_B)+1);
       ArrayResize(lnA_B_except,ArraySize(lnA_B_except)+1);
       ArrayResize(send_number,ArraySize(send_number)+1);
       ArrayResize(close_bucang,ArraySize(close_bucang)+1);
       
       orderA[ArraySize(orderA)-1]=result[0];
      
       py_orderid[ArraySize(py_orderid)-1]=result[1];
       lnA_B[ArraySize(lnA_B)-1]=result[2];
       lnA_B_except[ArraySize(lnA_B_except)-1]=result[3];
       send_number[ArraySize(send_number)-1]=result[4];
       close_bucang[ArraySize(close_bucang)-1]=float(result[5]);       
       
  
       
   //--- Now output all obtained strings
        
      //-order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);
     }
       printf("有历史没交易订单数");
   }

 void tickcheck()
{ string filename="tick.csv";
  int filehandle=FileOpen(filename,FILE_WRITE|FILE_CSV);  

update_data(filehandle,"AUDCAD");

FileClose(filehandle);
              }
//+------------------------------------------------------------------+

//+---获取价格数据写入外部文件
//+------------------------------------------------------------------+
void get_data()
{ string filename="price_record.csv";
  int filehandle=FileOpen(filename,FILE_WRITE|FILE_CSV);  

update_data(filehandle,"AUDCHF.lmx");
update_data(filehandle,"AUDNZD.lmx");
update_data(filehandle,"AUDUSD.lmx");
update_data(filehandle,"CADCHF.lmx");
update_data(filehandle,"EURAUD.lmx");
update_data(filehandle,"EURCAD.lmx");
update_data(filehandle,"EURCHF.lmx");
update_data(filehandle,"EURGBP.lmx");
update_data(filehandle,"EURNZD.lmx");
update_data(filehandle,"EURSGD.lmx");
update_data(filehandle,"EURUSD.lmx");
update_data(filehandle,"GBPAUD.lmx");
update_data(filehandle,"GBPCAD.lmx");
update_data(filehandle,"GBPCHF.lmx");
update_data(filehandle,"GBPUSD.lmx");
update_data(filehandle,"NZDUSD.lmx");
update_data(filehandle,"USDCAD.lmx");
update_data(filehandle,"USDCHF.lmx");
update_data(filehandle,"USDSGD.lmx");
update_data(filehandle,"AUDCAD.lmx");
//update_data(filehandle,"EURDKK.lmx");
update_data(filehandle,"GBPSGD.lmx");
update_data(filehandle,"NZDCAD.lmx");
update_data(filehandle,"NZDCHF.lmx");
update_data(filehandle,"NZDSGD.lmx");
//update_data(filehandle,"USDHKD.lmx");
//update_data(filehandle,"USDCNH.lmx");


                FileClose(filehandle);
                printf("打印数据");}
             
  void update_data(int filehandle,string name)
{  //多读几次，为了防止时间读错误或者为空
  // string str=name+","+string(iTime(name,15,0))+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2)+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2);
   string str=name+","+string(TimeLocal())+","+string( iOpen(name,0,0))+","+string(iClose(name,0,0));
    str=name+","+string(TimeLocal())+","+string( iOpen(name,0,0))+","+string(iClose(name,0,0));

 
   FileWriteString(filehandle,str+"\r\n");
 }
   void update_data_zhunbei(int filehandle,string name)
{  //多读几次，为了防止时间读错误或者为空
  // string str=name+","+string(iTime(name,15,0))+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2)+","+string((MarketInfo(name,MODE_ASK)+MarketInfo(name,MODE_BID))/2);
   string str=name+","+string(iTime(name,5,0))+","+string( iOpen(name,0,0))+","+string(iClose(name,0,0));
 

 }

//+------------------------------------------------------------------+
//+------------------------------------------------------------------+读取python文件函数

void read_API()
  {string filename="create.txt";
   string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];
   int filehandle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_TXT);
      while(!FileIsEnding(filehandle))
      {

         u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
         int k=StringSplit(FileReadString(filehandle),u_sep,result);
   //--- Show a comment 
     // printf(float(result[5]));
   //--- Now output all obtained strings
        order_send(result[0],float(result[1]),float(result[2]),string(result[3]),string(result[4]),float(result[5]),0.01,0);
        //         stockid ，    买入价，      卖出价   ，      订单号，          补仓点            多 or 空
      //-order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);
        
     }
     
       FileClose(filehandle);
       FileDelete(filename);
   }




//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+


//开仓需要 开仓的名称、期望对数差、期望平仓对数差、期望开仓时间
   //+------------------------------------------------------------------+建仓函数      
void order_send (string nameA,float open ,float except_close ,string orderid, string bucang ,float open_status,string open_number,string pre_orderid )
  { 
//--- 
      printf(orderid);
      int ticket_buy;
      int open_s;
      int open_s2;
      float bucangjiage;
      printf(open_status);
      if (open_status>0.5)
        {open_s=1;
        open_s2=9;
        bucangjiage=float(open)+float(bucang);}
      else
        {open_s=0;
         open_s2=10;
         bucangjiage=float(open) - float(bucang);
        }

      ticket_buy=OrderSend(nameA,open_s,open_number,MarketInfo(nameA,open_s2),3,0,0,"",1,0);
  //    printf(ticket_buy);
    //  printf(GetLastError());
      while(ticket_buy<0)
         {ticket_buy=OrderSend(nameA,open_s,open_number,MarketInfo(nameA,open_s2),3,0,0,"",1,0);}

       ArrayResize(orderA,ArraySize(orderA)+1);
       ArrayResize(py_orderid,ArraySize(py_orderid)+1);
       ArrayResize(lnA_B,ArraySize(lnA_B)+1);
       ArrayResize(lnA_B_except,ArraySize(lnA_B_except)+1);
       ArrayResize(send_number,ArraySize(send_number)+1);
       ArrayResize(close_bucang,ArraySize(close_bucang)+1);
       ArrayResize(orderB_A,ArraySize(orderB_A)+1);
       orderA[ArraySize(orderA)-1]=ticket_buy;
       py_orderid[ArraySize(py_orderid)-1]=orderid;
       lnA_B[ArraySize(lnA_B)-1]=open;
       lnA_B_except[ArraySize(lnA_B_except)-1]=except_close;
       send_number[ArraySize(send_number)-1]=open_number;
       close_bucang[ArraySize(close_bucang)-1]=bucangjiage;
       orderB_A[ArraySize(orderB_A)-1]=pre_orderid;
       FileWrite(filename_balance,string(ticket_buy)+","+string(orderid)+","+string(open)+","+string(except_close)+","+string(open_number)+","+string(bucang)+","+string(TimeCurrent())+","+string(pre_orderid));
 
     }
//+------------------------------------------------------------------+ 平仓交易函数                                     
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+



   void order_close()
  {

   for(int i=0;i<ArraySize(orderA);i++)
     {
      if(StringLen(orderA[i])>0)
       {
        string nameA="";
        string buy_ticket="";
        float ln_close=0;
        float buy_num;
        float open_type;
        float open_price;
        buy_ticket=orderA[i];
        ln_close=lnA_B_except[i];
        string orderB_A_ticket="";
        orderB_A_ticket=orderB_A[i];
        OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
        nameA=OrderSymbol();
        buy_num=OrderLots();
        open_type=OrderType();
         open_price=OrderOpenPrice();
        //平仓判断条件
         //printf(MathLog(MarketInfo(nameB,MODE_ASK))-MathLog(MarketInfo(nameA,MODE_BID)));
         //printf("close"+string(ln_close));

        if(MarketInfo(nameA,MODE_BID)>ln_close&&open_type==0)
         
          { int i_close=1;
       
          while(!OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_BID),0.01,Red)&&i_close<5)
          {OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_BID),0.01,Red);
           i_close=i_close+1;}
               for(int j=0;j<ArraySize(orderA);j++)
             {
              if(orderA[j]==orderB_A_ticket)
                {printf(string(j)+","+orderA[j]+","+orderB_A_ticket);
                 close_bucang[j]=open_price-0.001;
                }
             }
        //printf(GetLastError());
          tracking(orderA[i],"1"+","+py_orderid[i]+","+lnA_B[i]+","+lnA_B_except[i]); 
             orderA[i]="";
             py_orderid[i]="";
             lnA_B[i]="";
             lnA_B_except[i]="";
             send_number[i]="";
             close_bucang[i]="";
        }
        
         if(MarketInfo(nameA,MODE_ASK)<ln_close&&open_type==1)
         
          { int i_close=1;
       
          while(!OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_ASK),0.01,Red)&&i_close<5)
          {OrderClose(buy_ticket,buy_num,MarketInfo(nameA,MODE_ASK),0.01,Red);
           i_close=i_close+1;}
             for(int j=0;j<ArraySize(orderA);j++)
             { 
              if(orderA[j]==orderB_A_ticket)
                {printf(string(j)+","+orderA[j]+","+orderB_A_ticket);
                 close_bucang[j]=open_price+0.001;
                }
             }
        //printf(GetLastError());
          tracking(orderA[i],"1"+","+py_orderid[i]+","+lnA_B[i]+","+lnA_B_except[i]); 
             orderA[i]="";
             py_orderid[i]="";
             lnA_B[i]="";
             lnA_B_except[i]="";
             send_number[i]="";
             close_bucang[i]="";
        }
        
        
        
        
        
            } 
            
            
            
            
            
            
             }
              
              }
         
       


//+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//+------------------------------------------------------------------+ 计算止盈止损                                  
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+
//return 1 操作  return  0 不操作

void clac_stop()
{
   
   
    
       for(int i=0;i<ArraySize(orderA);i++)
       {  
       if(StringLen(orderA[i])>0)
          {
              string nameA="";
              double priceA_open="";
              string buy_ticket="";
              float ln_close=0;
              float buy_num;
              float open_type;
              float bucang;
              buy_ticket=orderA[i];
              ln_close=lnA_B_except[i];
              float bucangjiage=close_bucang[i];
              
                    OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
                    nameA=OrderSymbol();
                    priceA_open=OrderOpenPrice();
                    buy_num=OrderLots();
                    open_type=OrderType();
                   // printf(((MarketInfo(nameA,MODE_BID)-priceA_open)+(priceB_open-MarketInfo(nameB,MODE_ASK)))/(priceA_open+priceB_open));
              
              
              
               printf(nameA+","+string(bucangjiage)+","+string(float(float(tt[ArrayBsearch(tt,buy_num*100)+1])/100)));
               
               
               if(MarketInfo(nameA,MODE_BID)<bucangjiage &&open_type==0 )
                 {
 
                 order_send(nameA,bucangjiage,priceA_open,00000,string(priceA_open-bucangjiage),0.1,float(float(tt[ArrayBsearch(tt,buy_num*100)+1])/100),buy_ticket);
             
                   // printf(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red));

                 close_bucang[i]=0;
                 } 
            
               if(MarketInfo(nameA,MODE_ASK)>bucangjiage &&open_type==1 )
                 { 

                 order_send(nameA,bucangjiage,priceA_open,00000,string(bucangjiage-priceA_open),0.9,float(float(tt[ArrayBsearch(tt,buy_num*100)+1])/100),buy_ticket);
                 
                   // printf(!OrderClose(buy_ticket,0.01,MarketInfo(nameA,MODE_BID),0.01,Red));

                 close_bucang[i]=1000;
                 } 
           
           
           
           
           
           
           
           
            }  
         }
 
   

  }


void tracking(string buy_ticket,string tag)
{  string string_tracking="";
   OrderSelect(buy_ticket, SELECT_BY_TICKET,MODE_TRADES); 
   string_tracking=OrderSymbol()+","+OrderOpenPrice()+","+OrderOpenTime()+","+OrderClosePrice()+","+OrderCloseTime()+","+OrderLots()+","+OrderType()+","+OrderCommission()+","+OrderProfit()+",";
   string_tracking=string_tracking+tag;
   int filehandle=FileOpen("order/report_"+rand()+rand()+".csv",FILE_READ|FILE_WRITE|FILE_TXT);
   int size= FileSize(filehandle);
   FileSeek(filehandle, 0, SEEK_END);
   FileWrite(filehandle,string_tracking);
   FileClose(filehandle);
   }
   
   
   
   
//+------------------------------------------------------------------+ for lining baobiao                                   
 //+------------------------------------------------------------------+
//+------------------------------------------------------------------+




       
       
