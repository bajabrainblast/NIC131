'''
This file is dedicated to reading in the NIC131 dataset,
parsing the lines within, and outputting it to a simplified
pickle file. There will be multiple versions, organized in 
different ways.
'''

import pickle as pk
import nicStructures as nst

def isnum(string:str) -> bool:
    for ch in string:
        # if it is none of the accepted characters
        if (ch != '-' and ch != '0' and ch != '1' and ch != '2' and ch != '3' and ch != '4' and ch != '5' and ch != '6' and ch != '7' and ch != '8' and ch != '9'):
            return False
    return True

def read_station_head(sta:nst.Station, line:str):
    sta.line_head = line.strip()
    sta.name_full = line[0:10].strip()
    sta.name_station = line[0:5].strip()
    sta.name_country = line[5:10].strip()

    #try:
    substr = line[47:64]
    spl = substr.split()
    if len(spl) != 3:
        spl = substr.replace("-", " -").split()
    sta.latitude = int(spl[0])
    sta.longitude = int(spl[1])
    sta.altitude = int(spl[2])
    sta.region = int(line[78:])
    #except:
        #sta.need_fix = True
    
    return
    
def read_station_mean(sta:nst.Station, line:str):
    sta.line_mean = line
    spl = line.split()
    try:
        sta.mean_total = int(spl[-1])
        for i in range(12):
            ind = -2 - i
            sta.mean[11-i] = int(spl[ind])
    except:
        sta.need_fix = True
    return
    
def read_station_stdv(sta:nst.Station, line:str):
    sta.line_stdv = line
    spl = line.split()
    try:
        sta.stdv_total = int(spl[-1])
        for i in range(12):
            ind = -2 - i
            sta.stdv[11-i] = int(spl[ind])
    except:
        sta.need_fix = True
    return
    
def read_station_year(sta:nst.Station, line:str):
    yr = nst.Year()
    yr.line = line
    # get name and year
    yr.name = line[0:10]
    yr.year = int(line[10:14])
    spl = line[15:].split()
    # if breaks month pattern, dont bother
    if len(spl) != 13:
        yr.need_fix = True
        sta.need_year_fix = True
        sta.years.update({yr.year: yr})
        return
    # get month values
    for i in range(0, 12):
        yr.months[i] = int(spl[i+1])
    # get total
    yr.total = int(spl[12])
    sta.years.update({yr.year: yr})

def manual_handle_error(st:nst.Station):
    if st.need_year_fix:
        for key, val in st.years.items():
            if val.need_fix == True:
                print(val.line)
                inp = [int(x) for x in input("enter the monthly values followed by the total:\n\t").split()]
                for i in range(12):
                    val.months[i] = inp[i]
                val.total = inp[12]
        if "1" in input("enter 1 if year data was corrected: "):
            st.need_year_fix = False
    if st.need_fix:
        print(st.line_head)
        print(st.line_mean)
        print(st.line_stdv)
        inp = input("enter 1 for head error, 2 for mean, 3 for stdv, or any combination. example: 13\n\t")
        if "1" in inp:
            inp2 = input("enter the station name, country name, lat, lon, alt, and region number. if any fields not present, enter *\n\t").split()
            if inp2[0] != "*":
                st.name_station = inp2[0]
            if inp2[1] != "*":
                st.name_country = inp2[1]
            if inp2[2] != "*":           
                st.latitude = int(inp2[2])
            if inp2[3] != "*":
                st.longitude = int(inp2[3])
            if inp2[4] != "*":
                st.altitude = int(inp2[4])
            if inp2[5] != "*":
                st.region = int(inp2[5])
        if "2" in inp:
            inp2 = [int(x) for x in input("enter the monthly mean, followed by the total:\n\t")]
            for i in range(12):
                st.mean[i] = inp2[i]
        if "3" in inp:
            inp2 = [int(x) for x in input("enter the monthly stdv, followed by the total:\n\t")]
            for i in range(12):
                st.stdv[i] = inp2[i]
        st.need_fix = False

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
            if line == "":
                break
            read_station_head(cur_station, line)
            line = reader.readline()
            read_station_mean(cur_station, line)
            line = reader.readline()
            read_station_stdv(cur_station, line)
            line = reader.readline()
        # handle a year
        if line != "":
            read_station_year(cur_station, line)
            line = reader.readline()
        # end read in all years

    # check for errors
    for st in stations:
        manual_handle_error(st)

    # write results
    with open(out_file, "wb") as out:
        pk.dump(stations, out)

    return out_file

if (__name__ == "__main__"):
    print("Reading NIC131...")
    output_file = NIC_read()
    print("Output to", output_file)

    print("Reading data from ", output_file, "...", sep="")
    stations = []
    with open(output_file, "rb") as input_file:
        stations = pk.load(input_file)
    for st in stations:
        print(st)

    print("Goodbye!")