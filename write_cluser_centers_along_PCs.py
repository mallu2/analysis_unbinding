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
parser.add_argument("-f", "--fileTraj", help= "GROMACS .xtc Trajectory file.",type=str)
parser.add_argument("-s", "--tprfile", help= "GROMACS tpr file with .tpr file name extension.", type=str)
##parser.add_argument("-n", "--ndxfile", help= "GROMACS index file with .ndx file name extension.",
                #     type=str)
parser.add_argument("-name", "--name", help= "Name for the output files, according to the foleder",
                     type=str)
args=parser.parse_args()
print(args.folder)

"If you read the information from the file, you need to name the output pdb according to the PC1 value and dumb frame X"
def read_PC1_frames(txtfile):
    if args.name=='SymL':
        df=pd.read_csv(args.folder+txtfile,sep='|')
        for i in range(len(df)):
            line=df.iloc[i]
            PC_val=int(line['projection on eigenvector 1 (nm)'])
            if line['Sequence']=='SymL':
                Frame_id=int(line['center'])
                #os.system("echo 0|gmx_mpi trjconv -f %s -s %s -o %s_%s.pdb -n %s -dump %s" % (args.fileTraj,args.tprfile,args.name,PC_val,args.ndxfile,Frame_id))
                os.system("echo 0|gmx_mpi trjconv -f %s -s %s -o %s_%s.pdb -dump %s" % (args.fileTraj,args.tprfile,args.name,PC_val,Frame_id))
          
    elif args.name=='NOD':
        df=pd.read_csv(args.folder+txtfile,sep='|')
        for i in range(len(df)):
            line=df.iloc[i]
            PC_val=int(line['projection on eigenvector 1 (nm)'])
            if line['Sequence']=='NOD':
                Frame_id=int(line['NOD_center'])
                os.system("echo 0|gmx_mpi trjconv -f %s -s %s -o %s_%s.pdb -dump %s" % (args.fileTraj,args.tprfile,args.name,PC_val,Frame_id))
                #os.system("echo 24|gmx_mpi trjconv -f %s -s %s -o %s_%s.pdb -n %s -dump %s" % (args.fileTraj,args.tprfile,args.name,PC_val,args.ndxfile,Frame_id))

read_PC1_frames('Framex.txt')
