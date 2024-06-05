'''
This file is dedicated to reading in the NIC131 dataset,
parsing the lines within, and outputting it to a simplified
pickle file. There will be multiple versions, organized in 
different ways.
'''
import pickle as pk
import nicStructures as nst

def read_station_head(sta:nst.Station, line:str):
    sta.line_head = line

    
def read_station_mean(sta:nst.Station, line:str):
    sta.line_mean = line
    
def read_station_stdv(sta:nst.Station, line:str):
    sta.line_stdv = line
    
def read_station_year(sta:nst.Station, line:str):
    yr = nst.Year()
    yr.line = line
    # get name and year
    yr.name = line[0:10]
    yr.year = int(line[10:14])
    spl = line[15].split()
    # if breaks month pattern, dont bother
    if len(spl) != 13:
        yr.need_fix = True
        sta.need_year_fix = True
        sta.years.update({yr.year: yr})
        return
    # get month values
    for i in range(0, 12):
        yr.months[i] = int(spl[i+1])
        if yr.months[i] == 9999:
            yr.need_fix = True
            sta.need_year_fix = True
    # get total
    yr.total = int(spl[13])
    if yr.total == 99999:
        yr.need_fix = True
        sta.need_year_fix = True
    sta.years.update({yr.year: yr})

def NIC_read(inp_file:str = "data/NIC131.dat", out_file:str = "data/stations.pk") -> str:
    stations = []
    reader = open(inp_file)
    line = reader.readline()
    cur_station = nst.Station()

    read_station_head(cur_station, line)
    line = reader.readline()
    read_station_mean(cur_station, line)
    line = reader.readline()
    read_station_stdv(cur_station, line)
    line = reader.readline()

    # read in all years
    while line:
        # if encountered end of station data, add cur to list and prepare next station
        if (line[10:14] == "9999"):
            stations.append(cur_station)
            cur_station = nst.Station()
            line = reader.readline() # skip separator line
            read_station_head(cur_station, line)
            line = reader.readline()
            read_station_mean(cur_station, line)
            line = reader.readline()
            read_station_stdv(cur_station, line)
            line = reader.readline()
        # handle a year
        read_station_year(cur_station, line)
        line = reader.readline()

    # write results
    with open(out_file, "wb") as out:
        pk.dump(stations, out)

    return out_file

if (__name__ == "__main__"):
    print("Reading NIC131...")
    output_file = NIC_read()
    print("Output to", output_file)

    '''
    print("Reading data from ", output_file, "...", sep="")
    stations = []
    with open(output_file, "rb") as input_file:
        stations = pk.load(input_file)
    print(stations)
    '''

    print("Goodbye!")