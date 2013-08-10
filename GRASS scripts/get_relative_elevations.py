import grass.script as grass
import csv
import os
os.chdir("C:/repositories/codeRepo/sol")

# get the device ids
idvals = dict.keys(grass.vector_db_select('nodes@PERMANENT', 
                                          columns = 'deviceid')['values'])
minelevdict = {}
for id in idvals:
  # extract a point
  grass.run_command('v.extract', input='nodes@PERMANENT', output='anode@PERMANENT', 
                    type='point', where='deviceid = ' + str(id))
  # buffer the point
  grass.run_command('v.buffer', input='anode@PERMANENT', output='abuff@PERMANENT',
                    type='point', distance=1500)
  # add an attribute table (screw you GRASS!)
  grass.run_command('v.db.addtable', map='abuff@PERMANENT')
  # get the minimum elevation in the buffer zone
  grass.run_command('v.rast.stats', vector='abuff@PERMANENT', 
                    raster='BORR_DEM5ft@PERMANENT', colprefix='elev')
  # get the neighborhood minimum elevation
  minelevdict[id] = grass.vector_db_select('abuff@PERMANENT', 
                                      columns = 'elev_min')['values'][1][0]
  # clean up
  grass.run_command("g.remove", flags="f", vect="anode@PERMANENT,abuff@PERMANENT")
# export values to csv file
with open("minelevs1500ft.csv", "w") as outfile:
  w = csv.writer(outfile)
  w.writerow(['deviceid', 'nbhdminelev'])
  for key, val in minelevdict.items():
    w.writerow([key, val])