#Job Scheduler Unified
#-------------------------------------------------------------------------------
# Name:        Unified CFX job Scheduler program
# Purpose:     To launch simulation input files files of ANSYS CFX in a first-in-first-out manner 
#
# Author:      Shreyas Ragavan
#
# Created:     29-07-2015
# Copyright:   (c) Shreyas Ragavan 2015
# Licence:     Copy Right.
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

#Importing the required Libraries in Python
import os
import subprocess as sp
import time as t
import datetime as dt
import glob as glob
import re
import shutil as sh
import csv

# User Input for Folder Locations and other options
# The other cluster list is very important to prevent clashes where the same run runs on
# several clusters.
Queueing_sys_loc      = r"Q:\Queueing_sys" #Main location of the queuing system
admin_loc             = r"Q:\Queueing_sys\admin" # admin folder location
cluster_name          = r'CL2' #Name of this cluster
ansys_inst_loc        = r'C:\Program Files\ANSYS Inc\v145\CFX\bin\cfx5solve' 
hostlist_32           = r'-par-dist "Host 1*processor_number1, host 2* processor_number2"' #Hosts on which the simulation will run along with the number of partitions on each host.
other_cluster_list    = ['CL1']  # Enter list of clusters here like this ['CL2','CL3',xx..]
create_the_paths      = "No" #Yes - to create the paths required for the job scheduler to function and first runs.



#Creating the relative file paths based on the above main location inputs
status_loc            = os.path.join(admin_loc,'Running_%s.%s'%(cluster_name,'.txt'))
only_small_switch     = os.path.join(admin_loc,'onlysmall_%s.txt'%cluster_name)
pause_set_loc         = os.path.join(admin_loc,'pause_%s.txt'%cluster_name)
small_runs_loc        = os.path.join(Queueing_sys_loc,'Small_runs')
simworking_loc        = os.path.join(Queueing_sys_loc,'Working_loc')
priority_loc          = os.path.join(Queueing_sys_loc,'Priority')
normal_loc            = os.path.join(Queueing_sys_loc,'Normal')
long_loc              = os.path.join(Queueing_sys_loc,'Long')
completed_loc         = os.path.join(Queueing_sys_loc,'Completed')
master_logger_loc     = os.path.join(admin_loc,'Restricted')
#second_logger_loc     = os.path.join(Queueing_sys_loc,'Logger')

MP_working_loc        = os.path.join(simworking_loc,'Mnp_Working_loc')

pause_long            = os.path.join(admin_loc,'pauselong_%s'%cluster_name)

excess_size_loc       = os.path.join(Queueing_sys_loc,'Excess_size')


logger_loc            = os.path.join(Queueing_sys_loc,'Logger')


completed_loc         = os.path.join(Queueing_sys_loc,'Completed')
MP_completed_loc      = os.path.join(completed_loc,'MnP_Completed')



def make_path():
    os.mkdir(status_loc)
    os.mkdir(normal_loc)
    os.mkdir(priority_loc)
    os.mkdir(long_loc)
    os.mkdir(completed_loc)
    os.mkdir(simworking_loc)
    os.mkdir(admin_loc)
    os.mkdir(master_logger_loc)
    os.mkdir(logger_loc)


# Function to copy a file from Loc1 to Loc2
def copy_command(file_loc1, file_loc2):
    print "Moving File %s to %s .. .." %(file_loc1, file_loc2)
    os.system ("copy %s %s" %(file_loc1,file_loc2))

# Function to move the Folder
def move_folder(loc1,loc2):
    print "Moving Folder %s to %s....."%(loc1,loc2)
    sh.move(loc1, loc2)

# Function to move a file from Loc1 to Loc2
def move_command(file_loc1, file_loc2):
    print "Moving File %s to %s .. .." %(file_loc1, file_loc2)
    os.system ("move %s %s" %(file_loc1,file_loc2))
    print "Done.."

#Write individual BAT scripts for chosen def file and run it
def run_exec(variable,v2,v3):
    print "Creating the BAT file to launch the def file..\n"
    fbw=r'"%s"'%(variable)
    dt_log="%s_%s" %(dt.date.today(),t.strftime("%HHr-%Mmin-%Ssec"))
    temp2=os.path.join(v2,'job_%s_%s.BAT'%(dt_log,cluster_name))
    f=open(temp2,'w')
    f.write('rem Start of BAT File\nSet ANSWAIT=1\ncd "%s"\n"%s" -%s %s %s'%(v2,ansys_inst_loc,v3,fbw,hostlist_32))
    f.close()
    print "Done. Launching . . . ."
    sp.call(r'"%s"'%temp2)
    t.sleep(1)

#Function for deleting the older BAT files used to execute the simulation. Prevents Clutter.
def BAT_killer(variable):
    for variable in glob.glob('%s/*_%s.BAT'%(variable,cluster_name)):
        if os.path.isfile(variable):
            os.remove(variable)

#Functions for creating and deleting Flags for showing the simulation is running.
def flag_create(variable,v2):
    print "Creating the Flag for simulation run"
    stat_loc=os.path.join(v2,variable)
    f=open(stat_loc,'w')
    f.write("Running")
    f.close()

def flag_del(variable,v2):
    print "Deleting the Flag for simulation run"
    stat_loc=os.path.join(v2,variable)
    os.remove(stat_loc)


#Reading the list generated and passing the first def file to the main program.
#def list_reader(variable1):
#    print "Entered the list reader function... extracting & passing single file name to the main_prog"
#    f = open("%s"%(fdiff_loc),'r')
#    fnames1 = f.read().splitlines()
#    f.close()
#    main_prog(fnames1[0])


#Scans for res file matching the def file name and then an out file.
#If available, the res,def and out files are transfered to the completed folder.  
#If res file unavailable, def and out files remain in working_loc
def success_scan(variable1, variable2, variable3, v4):
    p2=glob.glob('%s/%s*.%s' %(variable1,variable2, variable3))
    #print p2
    if p2==[]:
        print "No %s file..."%variable3
        success_scan.scanperm='no'
        return success_scan.scanperm
    else:
        success_scan.scanperm='yes'        
        print "the matching %s file is %s" %(variable3,p2[0])
        move_command(p2[0],v4)
        return success_scan.scanperm


def mres_success_scan(variable1, variable2, v4):
    p3=glob.glob('%s\%s*' %(variable1,variable2))
    print "the matching folder is %s" %p3[0]
    for index, item in enumerate(p3):
        print "item is :%s"%item
        move_folder(p3[index],v4)

#List Creator for small runs. Checks file Size before proceeding..        
def list_creator_smallruns(variable1, variable2):
    print"variable 1 is %s"%variable1
    list_name='List_%s_%s.txt'%(variable2, cluster_name)
    list_loc=os.path.join(admin_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_%s.BAT'%cluster_name)
    print "Location of List creator Small Runs for %s - %s" %(cluster_name,variableA1)
    BC=open('%s'%variableA1,'w')
    BC.write('@echo off \ncd /d "%s"\ndir *.def *.mdef /OD /b /s > "%s"'%(variable1,list_loc))
    BC.close()
    t.sleep(2)
    os.popen('"%s"'%variableA1)
    t.sleep(2)
    LC=open(list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    #Q_logger(fnames1,variable2)
    print "Small runs priority list is %s"%fnames1
    if fnames1==[]:
        print "Small runs priority List is empty. Going to Priority"
        list_creator_priority(priority_loc,'Priority')
    else :
        if (os.stat("%s"%fnames1[0]).st_size<180000000):
            print "Small run file size is okay. Processing..."
            main_prog(fnames1[0],variable2)            
        else :
            print "Small Run File Size is Excess. Moving out.."            
            move_command(fnames1[0], excess_size_loc)
            print "Exiting.."
            t.sleep(1)
            exit()
            

#Creating BAT script for extracting the list of def files in the priority folder - sorted Date wise. If list is empty - move to Normal Folder
def list_creator_priority(variable1, variable2):
    print"variable 1 is %s"%variable1
    list_name='List_%s_%s.txt'%(variable2, cluster_name)
    print 
    list_loc=os.path.join(admin_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_%s.BAT'%cluster_name)
    print variableA1
    print "Created & Extracted variables and file names for BAT script. Writing the BAT script to list file names.."
    BC=open('%s'%variableA1,'w')
    BC.write('@echo off \ncd /d "%s"\ndir *.def *.mdef /OD /b /s >"%s"'%(variable1,list_loc))
    BC.close()
    t.sleep(2)
    os.popen('"%s"'%variableA1)
    t.sleep(2)
    LC=open(list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    print "Def/Mdef file to be run is finalised and being passed..."
    #Q_logger(fnames1,variable2, cluster_name)
    print "priority list is %s for %s"%(fnames1,cluster_name)
    if fnames1==[]:
        print "priority List is empty. Moving to the Normal Location..."
        list_creator_normal(normal_loc,'Normal')
    else :
        print "Priority list is not empty. Submitting file to main_prog..."
        main_prog(fnames1[0],variable2)

#Creating BAT script for extracting the list of def files in the normal folder - sorted Date wise
def list_creator_normal(variable1, variable2):
    list_name='List_%s_%s.txt'%(variable2, cluster_name)
    print "Getting list of files in the normal location..."
    admin_list_loc=os.path.join(admin_loc,list_name)
    #logger_list_loc=os.path.join(logger_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_%s.BAT'%cluster_name)
    BC=open('%s'%variableA1,'w')
    BC.write('@echo off\ncd /d "%s"\ndir *.def *.mdef /OD /b /s >"%s"'%(variable1,admin_list_loc))
    BC.close()
    t.sleep(3)
    os.popen('"%s"'%variableA1)
    t.sleep(3)
    LC=open(admin_list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    #Q_logger(fnames1,variable2)
    if fnames1==[]:
        print "Normal List is empty. Taking a Long status run"        
        list_creator_long(long_loc,'Long')
    #fchk=re.search(r'Q:\\Queueing_sys\\Normal\\MNP_Input', fnames1[0], flags=re.IGNORECASE)
    #if fchk:
        #MP_prog(fnames1[0])
    else:
        main_prog(fnames1[0],variable2)

#List Creator for Long Status Runs. Runs only if Small runs, priority and normal lists are empty.
def list_creator_long(variable1, variable2):
    print"variable 1 is %s"%variable1
    list_name='List_%s_%s.txt'%(variable2, cluster_name)
    list_loc=os.path.join(admin_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_CL1.BAT')
    print variableA1
    BC=open('%s'%variableA1,'w')
    BC.write('@echo off\ncd /d "%s"\ndir *.def *.mdef /OD /b /s >"%s"'%(variable1,list_loc))
    BC.close()
    t.sleep(1)
    os.popen('"%s"'%variableA1)
    t.sleep(2)
    LC=open(list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    #Q_logger(fnames1,variable2)
    print "Long status list is %s"%fnames1
    if fnames1==[]:
        print "Long List is empty"
        flag_del('%s_scan.txt'%cluster_name, admin_loc)
        exit()
    else :
        main_prog(fnames1[0],variable2)

#Main Program - gets variable (Def file name) from Priority first and if empty, from Normal
def main_prog(variable,variable2):        
    BAT_killer(simworking_loc)
    loc1='"%s"'%variable
    loc2='"%s"'%simworking_loc
    temp1=os.path.split(variable)
    fextension=os.path.splitext(temp1[1])[1][1:]
    runner_name=os.path.join(simworking_loc,temp1[1])
    move_command(loc1,loc2)
    print "\n\nFinished Moving file"
    if fextension=='mdef':
        foldpath=variable.split(".")[0]
        move_folder(foldpath,simworking_loc)
        print "\n\n Finished moving Folder for mdef.."
    flag_del('%s_scan.txt'%cluster_name,admin_loc)
    flag_create('status_%s.txt'%cluster_name,admin_loc)
    date_start ="%s" %(dt.date.today())
    time_start = "%s" %(t.strftime("%HHr-%Mmin-%Ssec"))
    #R_logger(variable)
    run_exec(runner_name,simworking_loc,fextension)
    t.sleep(1)
    flag_del('status_%s.txt'%cluster_name,admin_loc)
    date_end ="%s" %(dt.date.today())
    time_end = "%s" %(t.strftime("%HHr-%Mmin-%Ssec"))
    All_run_log(date_start,time_start, temp1[1],cluster_name,date_end,time_end,variable2)
    BAT_killer(simworking_loc)
    temp2=os.path.splitext(temp1[1])[0]
    success_scan(simworking_loc,temp2,'res',completed_loc)
    if success_scan.scanperm=='yes':
        success_scan(simworking_loc,temp2,'out',completed_loc)
        success_scan(simworking_loc,temp2,'def',completed_loc)
    else: print "Since Res file unavailable. Leaving def and out file in working_loc..."
    success_scan(simworking_loc,temp2,'mres',completed_loc)
    if success_scan.scanperm=='yes':
        success_scan(simworking_loc,temp2,'mdef',completed_loc)
        mres_success_scan(simworking_loc,temp2,completed_loc)
    else: print "Since MRes file unavailable. Leaving def and out file in working_loc..."
    


#Log creation for all the runs with start time, end time, cluster name and run name
def All_run_log(date_start,time_start, run_name,cluster_name,date_end,time_end, li_from):
    print "Entering the details for the run logger..."    
    master_logger_fn = os.path.join(master_logger_loc,'Log_runs_Raw.csv')
    with open(master_logger_fn, 'ab') as fp:
        a = csv.writer(fp, delimiter=',');
        data = [[date_start,time_start, run_name ,cluster_name,date_end,time_end, li_from]];
        a.writerows(data);
        fp.closed
    print "Copying Master log to secondary log"
    copy_command(master_logger_fn,logger_loc)
 

#Function for scanning if other cluster is scanning. Prevents Race condition.
def Scan_race(variable,var2):
    print "Function variable 2 is %s"%var2
    print "\nFunction variable 1 %s"%variable
    print "Number of Clusters registered is :%s" %len(var2)
    lister=var2
    print "Set the proxy cluster list length"
    print "length of Proxy cluster list named 'lister' is %s" %(len(lister))
    print "Scanning for Race conditions for each of the clusters"
    for index, item in enumerate(var2):
        print "item is :%s"%item
        print "index is :%s:"%index
        temp_list=os.path.join(admin_loc,item)
        lister[index]=temp_list+"_scan.txt"
        print "Location of the Scan flag of other : %s\n"%lister[index]
        #print "\n"
        if os.path.isfile(lister[index]):
            print "Race exists. RACE EXISTS..sleeping for 20\n"
            t.sleep(20)
        else:
            print " SAFE to Continue .... "
            


# Program Initialisation comments 
date_time_now ="%s_%s" %(dt.date.today(),t.strftime("%HHr-%Mmin-%Ssec"))
date_now= "%s" %dt.date.today()
time_now="%s"%(t.strftime("%HHr-%Mmin-%Ssec"))
print " ------------------------------------------------------------------------------------------"
print " ------------------------------------------------------------------------------------------"
print "\n\nJob Scheduler launched. \nFOR %s on < %s > at %s\n"%(cluster_name, date_now, time_now)
print "Checking Preliminaries."
print ". . . . . . ."

# Creating the folder structure if the user option is set as Yes
if create_the_paths=="Yes":
    print "Creating the paths option is True. print`Creating the Queueing system path and folders..."
    make_path()

#Program first checks if the Pause flag is up. If yes - program exits. 
#If No - program checks if the Run Flag is up or down. If down - moves to Priority list creation. If Up - Program exits.
fexist1=os.path.isfile('%s'%pause_set_loc)
print "Pause Status Set for %s ?%s" %(cluster_name,fexist1)
if (fexist1==True):
    print "Pause Request available. Exiting program immediately."
    exit()
else:
    print "No Pause ! Checking Current Run Status >> Only Small runs Switch >> Pause Long switch .."
    
fexist2=os.path.isfile('%s'%status_loc)
fexist3=os.path.isfile('%s'%only_small_switch)
fexist4=os.path.isfile('%s'%pause_long)
print "Current run Status File for %s Exists? %s" %(cluster_name, fexist2)
if (fexist2==True):
    print "Exiting program as run is on-going in this cluster."
    exit()
else:
    print "No Current Run on %s"%cluster_name
    print "Checking - Single CLuster mode is :%s" %fexist3
    print "Creating Current Scan Flag.."
    flag_create('%s_scan.txt'%cluster_name,admin_loc)
    print "Checking for Race Condition..."
    Scan_race(admin_loc,other_cluster_list)
    print "Run can start. Going to the Small Runs Priority folder..."
    list_creator_smallruns(small_runs_loc,'Small_Runs')