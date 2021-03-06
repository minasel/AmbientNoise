#!/usr/bin/env python
#Prepare a dataset for joint inversion with surface waves and RFs
#Using the Hermann joint96 codes

#Steps
#1 > Run dispersion_to_hermann_stations.m to create the surface wave inversion prep files
#specificially, this generates nnall.disp for each station and puts irt in a separate
#directory
#2 > Run this code, specifying the data directory containing the stacked RFs for each station (these
#will have been generated by funclab). This will make directories contining the relevant .SAC files
#The directory containing the surface wave setup should also be provided. The code will look in the
#relevant folders and extract the nnall.dps

# If there are multiple funclab projects, one will have to change the RF_data directory and run this code several times. The ghost dirs will get
# copied every time, but this does not take long


import glob
import os
import pandas as pd


def main():


    #Specify where the surface wave data is to be found - this was generated by the 'db_to_hermann.m' code and consists of directories with
    #the file nnall,dsp, which contains the phase velocities as a function of period
    surface_wave_data = "/home/rmartinshort/Documents/Berkeley/Ambient_Noise/Depth_invert/Station_grid/Alaska_stations_plus_ghost_Miller_RF_2.5_Stations_only"

    #Specify where the RF data is to be found. This consists of a series of *mean.SAC files output from funclab
    #RF_data = "/home/rmartinshort/Documents/Berkeley/funclab/Meghan_RFs/RF_log_miller.dat"
    RF_data = "/home/rmartinshort/Documents/Berkeley/funclab/RF_TA_2014_1.0/RAYP_BAZ_STACK"

    cwd = os.getcwd()

    os.chdir(RF_data)

    #Specify the directory where the joint project is to be run
    newdir = "/home/rmartinshort/Documents/Berkeley/Ambient_Noise/Depth_invert/Station_grid/Alaska_stations_plus_ghost_RF_1999_2017_ALL"

    if not os.path.exists(newdir):
        os.system('mkdir %s' %newdir)

     #Use station information in restrict_file to ensure that only certain stations are parsed

    gather_RF(newdir,surface_wave_data,restrict_file=None)


def gather_RF(indir,swave_dir,restrict_file=None):

    '''Create directories for each station and copy the corresponsing RF files'''

    cwd = os.getcwd()
    os.chdir(swave_dir)
    swavedata = glob.glob('*_*')

    print swavedata

    if restrict_file is not None:
          station_db = pd.read_csv(restrict_file,sep=' ',names=['Lon','Lat','tmp','Code','tmp2'])
          station_names = list(station_db.Code)
    else:
          station_names = None
   
    print station_names

    os.chdir(cwd)

    RFs = glob.glob('*mean.SAC')
    stnames = []

    for RFfile in RFs:
        stnameR = RFfile.split('_')[1]
        stationpart = RFfile.split('_')[1].split('-')
        stnameN = '_'.join(stationpart[:2])

        if stnameN not in stnames:
            stnames.append(stnameN)
            print stnameN

            #Copy the surface wave data we want to invert

            if (stnameN in swavedata):

                if not os.path.exists('%s/%s' %(indir,stnameN)):
                    os.system('mkdir %s/%s' %(indir,stnameN))

                #Copy all the stacked SAC files to this dir
                os.system('cp *%s*mean.SAC %s/%s' %(stnameR,indir,stnameN))

                print "Generated dir for %s/%s" %(indir,stnameN)
                os.system('cp %s/%s/nnall.dsp %s/%s' %(swave_dir,stnameN,indir,stnameN))
                print "Copied nall.disp from %s/%s" %(swave_dir,stnameN)

    #if ghost dirs exist in the surface wave dataset, copy them too
    for dirname in swavedata:
        if 'ghost' in dirname:
            os.system('cp -r %s/%s %s' %(swave_dir,dirname,indir))
            print "Copied ghost dir %s" %dirname





if __name__ == "__main__":

    main()
