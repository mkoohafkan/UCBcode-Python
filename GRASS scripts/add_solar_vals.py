# this script is used to extract the solar radiation values from the rasters 
# created by loop_solar.py at the node locations and export a table containing
# the data

import grass.script as grass
import string

# make copy of nodes point vector
grass.run_command("g.copy", vect = "nodes@PERMANENT,nodelocs")

doy = [9, 23, 37, 51, 65, 79, 93, 107, 121, 135, 149, 161, 172, 182, 191, 205, 
       219, 233, 247, 257, 266, 278, 289, 303, 317, 331, 344, 356, 365]
cols = string.join(['RADDOY' + str(i) for i in doy], ' DOUBLE PRECISION, ') + ' DOUBLE PRECISION'
outcols = string.join(['RADDOY' + str(i) for i in doy], ',')
# i is the day of year (DOY) 
for i in doy:
	# add the column
	grass.run_command("v.db.addcol", map = "nodelocs@PERMANENT", 
	                  columns = "RADDOY" + str(i) + " DOUBLE PRECISION")
	grass.run_command("v.what.rast", vect='nodelocs@PERMANENT', 
	                  rast="globrad_DOY" + str(i) + "_16ft@PERMANENT", 
					  col="RADDOY" + str(i) )
# save node data to file
grass.run_command("v.out.ascii", input = "nodelocs@PERMANENT", fs = ',', 
                  columns = outcols, output = 'noderad')
# remove created file
grass.run_command("g.remove", flags="f", vect="nodelocs@PERMANENT")