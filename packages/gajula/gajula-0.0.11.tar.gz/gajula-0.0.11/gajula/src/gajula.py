from datetime import datetime, timedelta, date, time
import random
import time
import pytz 
from pprint import pprint
    
class Time_Utils:
    def __init__(self):
        self.timezones = pytz.all_timezones

    def today(self,format='date'):
        '''
        returns today date in desired format
        '''
        if format == 'date':
            return datetime.today()
        if format == 'string':
            return datetime.today().isoformat()
    
    def time(self,format='time',timezone='Universal'):
        '''
        returns current time in desired timezone and format
        '''
        timestamp = self.tznow(timezone=timezone)
        if format == 'time':
            return timestamp.time()
        if format == 'string':
            return timestamp.time().isoformat()
    
    def now(self,
            format='datetime',
            string=False,
            strformat='%Y-%m-%d %H:%M:%S'):
        ts = datetime.now()
        if string:
            return ts.strftime(strformat)
        if format == 'datetime':
            return ts
        if format == 'unix':
            return int( time.mktime(ts.timetuple()) )
        else:
            return "Uknown format, supported datetime,unix"
    
    def utcnow(self,
            format='datetime',
            string=False,
            strformat='%Y-%m-%d %H:%M:%S'):
        
        ts = datetime.utcnow()
        if string:
            return ts.strftime(strformat)
        if format == 'datetime':
            return ts
        if format == 'unix':
            return int( time.mktime(ts.timetuple()) )
        
    def tznow(self,
            format='datetime',
            string=False,
            strformat='%Y-%m-%d %H:%M:%S',
            timezone='Universal'):
        
        if timezone not in self.timezones:
            pprint(self.timezones)
            raise ValueError("Invalid Timezone passed, refer above supported timezones")
        
        ts = datetime.now(pytz.timezone(timezone))
        if string:
            return ts.strftime(strformat)
        if format == 'datetime':
            return ts
        if format == 'unix':
            return int( time.mktime(ts.timetuple()) )
        
    def str_to_date(self,date_string:str)->date:
        '''
        supported string formats 
        2019-12-04
        20191204
        2021-W01-1
        return type datetime.date(2019, 12, 4)
        '''
        return date.fromisoformat(date_string)
        
    def str_to_time(self,time_string:str)->time:  # needs testing
        '''
        supported time_string formats
        04:23:01
        T04:23:01
        T042301
        04:23:01.000384
        04:23:01,000
        04:23:01+04:00 contains timezone
        04:23:01Z contains timezone
        04:23:01+00:00 contains timezone
        '''
        return time.fromisoformat(time_string)
    
    def to_datetime(self,timestamp)->datetime:
        '''
        supported datetime formats
        2011-11-04
        20111104
        2011-11-04T00:05:23
        2011-11-04T00:05:23Z contains timezone
        20111104T000523
        2011-W01-2T00:05:23.283
        2011-11-04 00:05:23.283
        2011-11-04 00:05:23.283+00:00 contains timezone
        2011-11-04T00:05:23+04:00 contains timezone
        or  UNIX timestamp
        '''
        if type(timestamp) == str:
            return datetime.fromisoformat(timestamp)
        if type(timestamp) == int or type(timestamp) == float:
            timestamp = int(timestamp)
            return datetime.utcfromtimestamp(timestamp)
        if type(timestamp) == datetime:
            return timestamp
        
    def to_unix(self,timestamp):
        '''
        takes a timestamp and converts into unix version
        supports:
            string
            datetime
        '''
        if type(timestamp) == datetime:
            return int( time.mktime(timestamp.timetuple()) )
        if type(timestamp) == str:
            timestamp = self.str_to_datetime(timestamp)
            return int( time.mktime(timestamp.timetuple()) )

    def change_tz(self,timestamp,timezone='Universal',format='%Y-%m-%d %H:%M:%S'):
        '''
        takes timestamp,timezone,format as arguments
        converts timestamp into desired timezone
        supports:
            String to string
            datetime to datetime
            unix to unix
        '''
        if timezone not in self.timezones:
            raise ValueError("timezone not found. check timezones attribute for supported timezones")
        
        if type(timestamp) == str:
            ts = self.to_datetime(timestamp)
            ts = ts.astimezone(pytz.timezone(timezone))
            return ts.strftime(format)

        if type(timestamp) == datetime:
            return timestamp.astimezone(pytz.timezone(timezone))
        
        if type(timestamp) == int or type(timestamp) == float:
            timestamp = int(timestamp)
            ts = self.to_datetime(timestamp)
            ts = timestamp.astimezone(pytz.timezone(timezone))
            return int( time.mktime(ts.timetuple()) )
        else:
            return "unknown timestamp type, check doc strings"
                       
    def second_now(self,timezone='Universal'):
        '''
        takes timezone and returns current second today
        '''
        now = self.tznow(timezone=timezone)
        return int((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
    
    def today_midnight(self,timezone='Universal'):
        '''
        returns timestamp today's midnight -> datetime object
        '''
        now = self.tznow(timezone=timezone)
        return now.replace(hour=0, minute=0, second=0, microsecond=0)

        
    def time_btw(self,timestamp_1,timestamp_2,value='secs'):
        '''
        returns values between two timestamps
        supports:
            datetime object
            datetime string
        '''
        if type(timestamp_1) == str:
            timestamp_1 = self.to_datetime(timestamp_1)
        if type(timestamp_2) == str:
            timestamp_2 = self.to_datetime(timestamp_2)

        if value == 'secs':
            return abs((timestamp_1 - timestamp_2))
        
        if value == 'minutes':
            return abs(int((timestamp_1 - timestamp_2)/60))
        
        if value == 'hours':
            return abs(int((timestamp_1 - timestamp_2)/3600))
        
        if value == 'days':
            return abs(int((timestamp_1 - timestamp_2)/86400))
        
        else:
            return "Unkown value type"
    
    def from_now(self,
                 timestamp,
                 weeks=0,
                 days=0,
                 hours=0,
                 minutes=0,
                 seconds=0):
        
        timestamp = self.to_datetime(timestamp)
        future_ts = timestamp + timedelta(weeks=weeks,days=days)
        return future_ts.replace(hour=future_ts.hour + hours,
                                    minute=future_ts.minute + minutes,
                                    second = future_ts.second + seconds)
          

    def random_datetime(self,future=True)->datetime:
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
        
    
timeutils = Time_Utils()
        
    
