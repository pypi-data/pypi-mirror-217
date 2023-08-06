from datetime import datetime, timedelta
import random
import time
import pytz 

class Timeutils:
    def __init__(self):
        self.timestamp = datetime.utcnow()
        self.all_timezones = pytz.all_timezones

    def test_function(self)->None:
        print("module installed correctly..")
        return 

    def time_now(self,timezone='Universal',format='default'):
        '''
        returns time in desired timezone in desired format. 
        '''
        if timezone not in self.all_timezones:
            raise ValueError("Time zone is not valid")
        if format == 'object':
            return datetime.now(pytz.timezone(timezone))
        if format == 'unix':
            dt =  datetime.now(pytz.timezone(timezone))
            return int( time.mktime(dt.timetuple()) )
        if format == 'default':
            return datetime.now(pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return datetime.now(pytz.timezone(timezone)).strftime(format)

    def utc_now(self,format='datetime'):
        '''
        returns UTC time now
        types = datetime, unix
        '''
        if format not in ['datetime','default','unix']:
            return datetime.utcnow().strftime(format)
        if format =='datetime':
            return datetime.utcnow()
        if format =='default':
            return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        if format =='unix':
            return int( time.mktime(datetime.utcnow().timetuple()) )
    
    def random_date(self,future=True)->datetime:
        '''
        returns a random date and time in the next 365 days. 
        future is true if passed false will give random date and time in past. 
        '''
        r_days = random.randint(0,7)
        r_weeks = random.randint(0,51)
        r_minutes = random.randint(0,60)
        if future:
            return datetime.utcnow() + timedelta(days=r_days,weeks=r_weeks,minutes=r_minutes)
        else:
            return datetime.utcnow() - timedelta(days=r_days,weeks=r_weeks,minutes=r_minutes)
        
    def convert_unix_to_datetime(self,unix,format='default'):
        '''
        converts integer unix timestamp into datetime format
        '''
        unix = int(unix)

        if format not in ['default',None]:
            return datetime.utcfromtimestamp(unix).strftime(format)
        
        if format == None:
            return datetime.utcfromtimestamp(unix)
        
        if format == 'default':
            return datetime.utcfromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S')
        
    def convert_datetime_to_unix(self,timestamp):
        '''
        converts datetime into unix timestamp integer
        '''
        return int( time.mktime(timestamp.timetuple()) )
    
timeutils = Timeutils()

    
        