
import netCDF4 as nc
import csv

#global variables
NetCDF_fileName = "ersst.v4.201705.nc"
purpose = ("This data can be used to determine" +
			" and plot average Ocean temperatures"
)

#extracts necessary information from NetCDF file
#writes to two .csv files
def netCDFfetch(fileName):
	data = nc.Dataset(fileName)
	#prints dataset variables for reference
	print data.variables

	#Create and Handle .csv file
	csvFile = create_and_clear_csv(fileName + ".csv")
	#column names for csv file
	csv_header = ("Temperature, Latitude," + 
		"Longitude, Altitude, Time, Pressure \n"
	)
	csvFile.write(csv_header)
	#creates and fills ReadMe .csv file
	csvReadMe = create_and_clear_csv(fileName + "_ReadMe.csv")
	line = ("Abstract:," + data.summary + "\n" 
		"Purpose:," + purpose + "\n" +
		"License:," + data.license + "\n\n\n" + 
		"Legend," +
		"Temperature: Given in Celcius," +
		"Latitude: " + data["lat"].grids + "," +
		"Longitude: " + data["lon"].grids + "," +
		"Altitude: " + data["lev"].long_name + "," +
		"Time: " + data["time"].units + "," +
		"Pressure: n/a"
	)
	csvReadMe.write(line)

	#counters used to splice arrays
	lat_count = 0
	lon_count = 0
	temp = 0
	line = ""

	#loop through coordinates and get sea temp. to .csv
	for lat in data["lat"]:
		for lon in data["lon"]:
			temp = data["sst"][0, 0, lat_count, lon_count]
			line = (str(temp) + ", " + str(lat) + ", " + 
				str(lon) + ", 0, 0, Null\n" 
			)
			csvFile.write(line)
			#increment counter
			lon_count = lon_count + 1
		#increment and reset counters
		lat_count = lat_count + 1
		lon_count = 0

	#close files
	csvFile.close
	csvReadMe.close
	data.close()

#Param fileNameLocation
#	String fileName for pulling csv file
#	
#RETURN:
#	Returns an empty CSV file
#
def create_and_clear_csv(fileNameLocation):
	#clears csv file
	open(fileNameLocation, "w").close()
	return open(fileNameLocation,"w")

if __name__ == "__main__":
	netCDFfetch("../Data/" + NetCDF_fileName)






