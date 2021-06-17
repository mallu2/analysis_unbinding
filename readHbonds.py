#!/usr/bin/python3.6

import pandas as pd
import sys
import glob
import os
import argparse

#args.folder=sys.argv[1]
parser = argparse.ArgumentParser()
parser.add_argument("-fo", "--folder", help= "Path to the directory with hbonds-record and trajectory file in subfolders N/analysis/ana where N is the replica index.",
                     type=str)
parser.add_argument("-s", "--tprfile", help= "GROMACS tpr file with .tpr file name extension.", type=str)
parser.add_argument("-n", "--ndxfile", help= "GROMACS index file with .ndx file name extension.",
                     type=str)
parser.add_argument("-name", "--name", help= "Name for the output files, according to the foleder",
                     type=str)
args=parser.parse_args()
print(args.folder)

class read_ana:
	"""This class reads different output files from gromacs analysis"""
    def __init__(self,name):
        self.name = name
    @classmethod
    #method to geth replica
    def get_names(cls,name):
        "Get all subfolders with different replica"
        if name=='DBDA':
            name= 'DBDA_rmsd.xvg'
        if name=='NMR_DBDA':
            name= 'NMR_DBDA_rmsd.xvg'
        if name=='DBDB':
            name= 'DBDB_rmsd.xvg'
        if name=='coA':
            name= 'coreA_rmsd.xvg'
        if name=='coB':
            name= 'coreB_rmsd.xvg'
        if name=='DNA':
            name='DNA_rmsd.xvg'
        if name=='DNAf':
            name='Flux_DNA.xvg'
        if name=='Protf':
            name='Flux_Protein.xvg'
        if name=='avgdis':
            name='draver.xvg'
        if name=='maxdis':
            name='drmax.xvg'
        if name=='CG':
            name='CG_dist.xvg'
        if name=='hPP':
            name='hbnum_Pro-Pro.xvg'
        if name=='hDP':
            name='hbnum_DNA-Pro.xvg'
        return(cls(name))

    @staticmethod
    #method to get the replica for the trajectory
    def get_replica_traj(folder,name):
        name = read_ana.get_names(name).name
        "Get all subfolders with different replica"
        files = glob.glob(folder+'*/analysis/ana/'+name)
        files.sort()
        return(files)
    @staticmethod
    #get df of hydrogenbonds, the last frame and the corresponding trajectory 
    def get_traj_unbind(folder):
        files_Hb_DP=read_ana.get_replica_traj(folder,'hDP')
        files_traj=read_ana.get_replica_traj(folder,'md_compact_noWater.xtc')
        print(files_Hb_DP) #check the order. You need to make sure that you track the Hbonds for the right trajectory.
        "Get df from file and get the last frame."
        for i in range(len(files_Hb_DP)):
            fileHb=files_Hb_DP[i]
            fileTraj=files_traj[i]
            print((fileHb,fileTraj))
            df=pd.read_csv(fileHb, sep='\s+',skiprows=25,names=['Frame','Num','P35'])
            df['Num']=df['Num'].rolling(window=100).mean()
            if (df['Num']<7).any():
                list_below=df[df['Num']<7]
                first_frame_below_10=list(list_below['Frame'])[0]
            else:
                first_frame_below_10='300000' 
            print(first_frame_below_10)
            os.system("echo 13 13|gmx_mpi trjconv -f %s -s %s -o %s_%s.xtc -fit rot+trans -n %s -e %s" % (fileTraj,args.tprfile,args.name,i,args.ndxfile,first_frame_below_10))
read_ana.get_traj_unbind(args.folder)



