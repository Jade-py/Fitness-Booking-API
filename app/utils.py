import pytz

# Timezone handling in UTC for standardization
def convert_timezone(dt, from_tz='Asia/Kolkata', to_tz='UTC'):
    ist = pytz.timezone(from_tz)
    target = pytz.timezone(to_tz)
    return ist.localize(dt).astimezone(target)
