#!/usr/bin/env python
#RMS Oct 2017
#Make database from hermann inversion using station locations - ready for a joint inversion with receiver functions
#This enters the dirctory containing the station names and then extracts the Vs vs depth profiles to one file

import glob
import os
import pandas as pd
import sys

def main():

       try:
          datadir = sys.argv[1]
       except:
          print "datadir not provided at command line. Using defaults (hard coded)"

          #This is where the files will be located
          datadir = "/home/rmartinshort/Documents/Berkeley/Ambient_Noise/Depth_invert/Station_grid/Alaska_stations_400"
          datadir = "/home/rmartinshort/Documents/Berkeley/Ambient_Noise/Depth_invert/Station_grid/Alaska_stations_plus_ghost_400_AK_TA2"
          datadir = "/home/rmartinshort/Documents/Berkeley/Ambient_Noise/Depth_invert/Station_grid/Alaska_stations_plus_ghost_Miller_RF_2.5_Stations_only"

       cwd = os.getcwd()

       if not os.path.exists(datadir):
            print "Provided dir %s does not exist!" %datadir
            sys.exit(1)

       os.chdir(datadir)

       stationsfile = "Alaska_stations.txt"

       #Load the station database and loop through, find the station and append to the database
       station_db = pd.read_csv(stationsfile,sep=' ',names=['Lon','Lat','tmp','Code','tmp2'])

       if os.path.exists('alaskastations.3d.mod'):
          os.system('rm alaskastations.3d.mod')

       for index, row in station_db.iterrows():

            dirname = row.Code
            stlon = row.Lon + 360.0
            stlat = row.Lat

            print dirname,stlon,stlat
            if os.path.isdir(dirname):

               #Enter directory, append data to the database and move on

               os.system("awk 'BEGIN{depth=0} {if (NR >= 13) print '%s','%s', depth, $3} {depth=depth+$1}'\
               %s/end.mod >> alaskastations.3d.mod" %(stlon,stlat,dirname))

       os.system("awk '{if ($3 <= 200) print $0}' alaskastations.3d.mod > alaskastations.3d.mod.reduced")

       os.chdir(cwd)




if __name__ == "__main__":

    main()
