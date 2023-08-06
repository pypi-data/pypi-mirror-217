from datetime import datetime, timedelta, date, time
import random
import time
import pytz 
from pprint import pprint
    
class TimeUtils:
    '''
    timeutils class packages useful functions for devs
    please doc strings for better understading
    TS: timestamp
    Functions:
        today : returns today date object or string
        time : returns time in given timezone in object or string
        now: returns local TS in desired format object, string, UNIX
        utcnow: same as now but in UTC
        tznow: same as above but given timezone
        str_to_date: takes string and returns date object
        str_to_time: takes string and returns time object
        to_datetime: takes string or UNIX and returns TS object
        to_unix: takes string or TS object and returns UNIX TS
        change_tz: takes string or UNIX or TS object and changes to desired timezone
                    String -> string
                    TS object -> TS object
                    UNIX -> UNIX
        second_now: returns current second in the day
        today_midnight: returns today midnight TS object
        time_btw: takes 2 timestamps returns time gap (secs, minutes, hours, days, weeks)
        ts_from_now:(-past and +future ) takes timestamp and gives next timestamp 
                    in given weeks, days, hours, minutes, secs
        weekdays_btw: takes 2 dates and returns weekday (monday,sunday,3,4) Monday = 0
        weekends_btw: takes 2 dates and returns weekends in between
        workdays_bw: takes 2 dates and returns working days between 
        ALL THREE above support string or date object.
        random_ts: returns random timestamp in future or past


    '''
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
    
    def ts_from_now(self,
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
    def _conv_dates(self,start,end):
        '''
        Takes start date and end date:
        supported_input:
            date object
            string
            UNIX timestamp
        returns date object
        '''
        # for string type inputs
        if type(start) == str:
            start = self.str_to_date(start)
        if type(end) == str:
            end = self.str_to_date(end)

        # for unix inputs
        if type(start) == int:
            start = self.to_datetime(start)
            start = start.date()

        if type(end) == int:
            end = self.to_datetime(start)
            end = end.date()

        return start,end

    
    def weekdays_btw(self,start,end,weekday='sunday'):
        '''
        Takes start date and end date:
        supported_input:
            date object
            string
            UNIX timestamp
        returns all occuring week days in between those two dates.
        '''
        start,end  = self._conv_dates(start,end)
        
        # select the weekday
        if weekday == 'monday' or weekday == 0:
            weekday = 0
        if weekday == 'tuesday' or weekday == 1:
            weekday = 1
        if weekday == 'wednesday' or weekday == 2:
            weekday = 2
        if weekday == 'thursday' or weekday == 3:
            weekday = 3
        if weekday == 'friday' or weekday == 4:
            weekday = 4
        if weekday == 'saturday' or weekday == 5:
            weekday = 5
        if weekday == 'sunday' or weekday == 6:
            weekday = 6

        total_days: int = (end - start).days + 1
        all_days = [start + timedelta(days=day) for day in range(total_days)]
        return [day for day in all_days if day.weekday() is weekday]
          
    def weekends_btw(self,start,end):
        '''
        Takes start date and end date:
        supported_input:
            date object
            string
            UNIX timestamp
        returns all occuring weekends in between those two dates.
        '''
        # for string type inputs
        start,end  = self._conv_dates(start,end)
        
        total_days: int = (end - start).days + 1
        all_days = [start + timedelta(days=day) for day in range(total_days)]
        return [day for day in all_days if day.weekday() is [5,6]]

    def workdays_btw(self,start,end):
        '''
        Takes start date and end date:
        supported_input:
            date object
            string
            UNIX timestamp
        returns all occuring weekends in between those two dates.
        '''
        start,end  = self.conv_dates(start,end)
        
        total_days: int = (end - start).days + 1
        all_days = [start + timedelta(days=day) for day in range(total_days)]
        return [day for day in all_days if day.weekday() is [0,1,2,3,4]]
    

    def random_ts(self,future=True)->datetime:
        '''
        returns a random date and time in the next 365 days. 
        future is true if passed false will give random date and time in past. 
        '''
        r_days = random.randint(0,7)
        r_weeks = random.randint(0,999)
        r_minutes = random.randint(0,60)
        if future:
            return datetime.utcnow() + timedelta(days=r_days,weeks=r_weeks,minutes=r_minutes)
        else:
            return datetime.utcnow() - timedelta(days=r_days,weeks=r_weeks,minutes=r_minutes)
        
    
timeutils = TimeUtils()
        
    
