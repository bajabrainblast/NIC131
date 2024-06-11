class Region:
    def __init__(self):
        self.number = 0             # region number
        self.stations = {}          # all stations, indexed by station name
        self.yearly_averages = {}   # every year's average, indexed by year

class Station:
    def __init__(self):
        self.name_full = ""         # 10ch combination of station and country
        self.name_station = ""      # 5ch station 
        self.name_country = ""      # 5ch country
        self.region = 0             # region number
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.need_fix = False
        self.mean = [0] * 12        # monthly mean
        self.mean_total = 0
        self.stdv = [0] * 12        # monthly standard deviation
        self.stdv_total = 0
        self.years = {}             # list of years, indexed by year
        self.need_year_fix = False
        self.average = 0            # station average
        self.line_head = ""
        self.line_mean = ""
        self.line_stdv = ""
    def __str__(self) -> str:
        return self.name_full

class Year:
    def __init__(self):
        self.name = ""              # name
        self.year = 0               # year
        self.months = [0] * 12      # each month
        self.need_fix = False
        self.total = 0              # total
        self.line = ""

