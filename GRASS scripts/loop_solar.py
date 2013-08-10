# this script is used to run the GRASS module r.sun in a loop
# for the specified sequence of days

import grass.script as grass
import os
os.chdir("C:/repositories/codeRepo/sol")

doy = range(1, 366)
#doy = [9, 23, 37, 51, 65, 79, 93, 107, 121, 135, 149, 161, 172, 182, 191, 205, 
#       219, 233, 247, 257, 266, 278, 289, 303, 317, 331, 344, 356, 365]
# i is the day of year (DOY) to use for running r.sun
for i in doy:
	# want to get insolation time, global radiation
	insolname = "insol_DOY" + str(i) + "_16ft"
	radname = "globrad_DOY" + str(i) + "_16ft"
	# run the solar model
	grass.run_command("r.sun", flags = "s",
					  elevin = "BORR_DEM16ft@PERMANENT", 
					  aspin = "aspect_16ft@PERMANENT", 
					  slopein = "slope_16ft@PERMANENT",
					  insol_time = insolname, glob_rad = radname, day = i)
	# export the outputs to GTiff files
	grass.run_command("r.out.gdal", input = insolname + "@PERMANENT", output = insolname)
	grass.run_command("r.out.gdal", input = radname + "@PERMANENT", output = radname)