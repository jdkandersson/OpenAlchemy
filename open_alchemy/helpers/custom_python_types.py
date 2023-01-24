import datetime
import re

class duration(datetime.timedelta):
    # duration (ISO 8601)
    def fromisoformat(duration_string):
        # adopted from: https://rgxdb.com/r/SA5E91Y
        regex_str = r'^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$'
        validation = re.match(regex_str, duration_string)
        if validation:
            groups = validation.groups()
            
            # timedelta does not support years and months
            # => approximate, since the actual calendar time span is not known
            years_in_days = int(groups[0]) * 365 if groups[0] else 0
            months_in_days = int(groups[1]) * 30 if groups[1] else 0
            
            timedelta = {
                'days': years_in_days + months_in_days + (int(groups[2]) if groups[2] else 0),
                'hours': int(groups[3]) if groups[3] else 0,
                'minutes': int(groups[4]) if groups[4] else 0,
                'seconds': int(groups[5]) if groups[5] else 0
            }
            
            return datetime.timedelta(**timedelta)
        else:
            raise ValueError(f'Invalid isoformat string: {duration_string!r}')
    
    def isoformat(td_object: datetime.timedelta) -> str:
        def zero_is_empty(int_to_str, concat):
            if int_to_str != 0:
                return str(int_to_str) + concat
            else:
                return ''
                
        PY = td_object.days // 365
        PM = (td_object.days - PY * 365) // 30
        PD = (td_object.days - PY * 365 - PM * 30)
        
        P = [zero_is_empty(PY,'Y'), zero_is_empty(PM,'M'), zero_is_empty(PD,'D')]
        
        TS = td_object.seconds
        TH, TS = divmod(TS, 3600)
        TM, TS = divmod(TS, 60)
        
        T = [zero_is_empty(TH,'H'), zero_is_empty(TM,'M'), zero_is_empty(TS,'S')]
        
        return 'P' + ''.join(P) + 'T' + ''.join(T)    