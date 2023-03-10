from datetime import datetime, timedelta
from peskos._config import days_of_week
from peskos.models.client import Clients
from peskos.models.trading_records import TradingRecords
from peskos.models.verified_records import VerifiedRecords


time_type = {
   "weekly": 4,
   "monthly": 19,
   "yearly": 239
}

def calc_date(_date:datetime, ticket_type:str) -> list:
   trading_days = list()
   trading_days.append(_date)
   count = 0

   while count < time_type[ticket_type]:
      if days_of_week[trading_days[-1].isoweekday()] in ["saturday", "sunday"]:
         trading_days.append(trading_days[-1] + timedelta(days=1))
         continue
      trading_days.append(trading_days[-1] + timedelta(days=1))
      count += 1
   return trading_days
            

def checkrecords(client:Clients, ticket_type:str):
   # check if the user has a record on the verified record list
   # get the date in which the user was last added and check if it's a weekend
   # strip weekends and add 4 days on top
   client_records = TradingRecords.query.filter_by(account_number=client.account_number)
   vclient = VerifiedRecords.query.filter_by(client_id=client.id).all()

   if not client_records.all():
      return False

   if not vclient:
      # if no vclient, it means the client is yet to start their first trading or yet to be initiated
      # enter the database get the users first record and get the date
      # use the date object to get the day the user started 
      client = client_records.first()
      # now grab the payment date and check if there is any data in database matching 
      # account number and client number
      paydays = calc_date(client.date_entered, ticket_type)
      tpay = TradingRecords.query.filter_by(account_number=client.account_number, date_entered=paydays[-1]).first()
      return tpay

   # Get the last verified date from the last verified record
   # Get the next evaluation day and return to the user

   last_verified_record = vclient[-1].date_initiated
   paydays = calc_date(last_verified_record)
   # print(paydays)
   tpay = TradingRecords.query.filter_by(account_number=client.account_number, date_entered=paydays[-1]).first()
   # print(tpay)
   return tpay




 # dummy_data = [
    #     {
    #         "name": "hanslett junior",
    #         "account_number":  "sdfsf2334",
    #         "initial_amount": 2000,
    #         "final_amount": 3000,
    #         "profit": 1000,
    #         "acc_statement": "Here is a statement",
    #         "date_entered": datetime.utcnow().date() 
    #     },
    #     {
    #         "name": "hanslett junior",
    #         "account_number":  "sdfsf2334",
    #         "initial_amount": 2000,
    #         "final_amount": 3000,
    #         "profit": 1000,
    #         "acc_statement": "Here is a statement",
    #         "date_entered": datetime.utcnow().date() + timedelta(days=1) 
    #     },
    #     {
    #         "name": "hanslett junior",
    #         "account_number":  "sdfsf2334",
    #         "initial_amount": 2000,
    #         "final_amount": 3000,
    #         "profit": 1000,
    #         "acc_statement": "Here is a statement",
    #         "date_entered": datetime.utcnow().date() + timedelta(days=2) 
    #     },
    #     {
    #         "name": "hanslett junior",
    #         "account_number":  "sdfsf2334",
    #         "initial_amount": 2000,
    #         "final_amount": 3000,
    #         "profit": 1000,
    #         "acc_statement": "Here is a statement",
    #         "date_entered": datetime.utcnow().date() + timedelta(days=3) 
    #     },
    #     {
    #         "name": "hanslett junior",
    #         "account_number":  "sdfsf2334",
    #         "initial_amount": 2000,
    #         "final_amount": 3000,
    #         "profit": 1000,
    #         "acc_statement": "Here is a statement",
    #         "date_entered": datetime.utcnow().date() + timedelta(days=4) 
    #     }
    # ]
    # for data in dummy_data:
    #     nws = TradingRecords(**data)
    #     db.session.add(nws)
    #     db.session.commit()