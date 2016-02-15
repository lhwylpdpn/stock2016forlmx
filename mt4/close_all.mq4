//+------------------------------------------------------------------+
//|                                                     testnet2.mq4 |
//|                        Copyright 2015, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2015, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
  test2();
  }
//+------------------------------------------------------------------+


void test2()
{  int total=OrdersTotal();
printf(total);
for(int i=0;i<total;i++)
  {printf(OrderSelect(i,SELECT_BY_POS));
   int type;
   printf(OrderTicket());
    if(OrderType()==0)
          {
           type=9;
          }
       if(OrderType()==1)
          {
           type=10;
          }
   OrderClose(OrderTicket(),OrderLots(),MarketInfo(OrderSymbol(),type),100,Red);
  }


}