#-------------------------------------------------------------------------------
# Name:        CFX job Scheduler
# Purpose:     Program to run priority level and normal level simulations in a First-in-first-out manner
#
# Author:      Shreyas Ragavan
#
# Created:     28-05-2014
# Copyright:   (c) Shreyas Ragavan 2014
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

#Setting the required Folder paths/locations. Use this list to change paths to folders.
status_loc=r"Q:\Queueing_sys\admin\status2.txt"
status_other_loc=r"Q:\Queueing_sys\admin\status1.txt"
excess_size_loc=r"Q:\Queueing_sys\Excess_size_NotInUse"
pause_set_loc=r"Q:\Queueing_sys\admin\pause2.txt"
small_runs_loc=r"Q:\Queueing_sys\Small_runs"
simworking_loc=r"Q:\Queueing_sys\working_loc"
admin_loc=r"Q:\Queueing_sys\admin"
logger_loc=r"Q:\Queueing_sys\logger"
priority_loc=r"Q:\Queueing_sys\Priority"
normal_loc=r"Q:\Queueing_sys\Normal"
long_loc=r"Q:\Queueing_sys\Long"
completed_loc=r"Q:\Queueing_sys\Completed"
single_cl_mode_loc=r"Q:\Queueing_sys\admin\onlyone.txt"
hostlist_32=r'-par-dist "XX1*N, XX2*N2, XX3*N3, XX4*N4"'
ansys_inst_loc=r'C:\Program Files\ANSYS Inc\v145\CFX\bin\cfx5solve'

def move_command(file_loc1, file_loc2,current_location):
    os.chdir(current_location)    
    print "Moving File %s to %s .. .." %(file_loc1, file_loc2)
    os.system ("move %s %s" %(file_loc1,file_loc2))

#Creating a log/status file to show which run is currently going on.
def R_logger(variable):
    logrun_loc=os.path.join(admin_loc,'Current_Job.html')
    run_name=os.path.split(variable)
    dt_log="%s_%s" %(dt.date.today(),t.strftime("%HHr-%Mmin-%Ssec"))
    run_writer=open(logrun_loc,'w')
    run_writer.write("<b> Ongoing Run Start:</b><br/>%s<br/><br/>%s"%(dt_log,run_name[1]))
    run_writer.close()
    os.system
    
#Creating a log/status file to show which runs are pending.
def Q_logger(variable1,variable2):
    logf_loc=os.path.join(logger_loc,'Queue_%s.html'%variable2)
    log_writer=open('%s'%logf_loc,'w')
    log_writer.write("<b>%s Runs Queue Status<br/>%s<br/></b><br/><br/>Jobs pending :<br/>"%(variable2,dt.datetime.now()))
    if (len(variable1)==0 or len(variable1)==1):
        log_writer.write('<br/>...No further Runs waiting to be Queued!')
    else:
        i=1
        while i<len(variable1):
            Qtempname=os.path.split(variable1[i])
            log_writer.write('%s<t/>%s<br/>'%(i,Qtempname[1]))
            i+=1
    log_writer.close()


#Write individual BAT scripts for each def file and run it
def run_exec(variable):
    fbw=r'"%s"'%(variable)
    dt_log="%s_%s" %(dt.date.today(),t.strftime("%HHr-%Mmin-%Ssec"))
    temp2=os.path.join(simworking_loc,'job_%s_CL2.BAT'%dt_log)
    f=open(temp2,'w')
    f.write('rem Start of BAT File\n@Echo off\nSet ANSWAIT=1\ncd "%s"\n"%s" -def %s %s'%(simworking_loc,ansys_inst_loc,fbw,hostlist_32))
    f.close()
    sp.call(r'"%s"'%temp2)
    t.sleep(1)

#Creating BAT script for extracting the list of def files in the normal folder - sorted Date wise
def list_creator_normal(variable1, variable2):
    list_name='List_%s.txt'%variable2
    admin_list_loc=os.path.join(admin_loc,list_name)
    logger_list_loc=os.path.join(logger_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_CL1.BAT')
    BC=open('%s'%variableA1,'w')
    BC.write('@Echo off\ncd /d " "%s"\ndir *.def /OD /b >"%s"'%(variable1,admin_list_loc))
    BC.close()
    t.sleep(3)
    os.popen('"%s"'%variableA1)
    t.sleep(3)
    LC=open(admin_list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    Q_logger(fnames1,variable2)
    if fnames1==[]:
        print "Normal List is empty. Taking a Long status run"        
        list_creator_long(long_loc,'Long')
    else :
        main_prog(fnames1[0],normal_loc)

#Creating BAT script for extracting the list of def files in the priority folder - sorted Date wise. If list is empty - move to Normal Folder
def list_creator_priority(variable1, variable2):
    print"variable 1 is %s"%variable1
    list_name='List_%s.txt'%variable2
    list_loc=os.path.join(admin_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_CL2.BAT')
    print variableA1
    BC=open('%s'%variableA1,'w')
    BC.write('@Echo off\ncd /d " "%s"\ndir *.def /OD /b /s >"%s"'%(variable1,list_loc))
    BC.close()
    t.sleep(2)
    os.popen('"%s"'%variableA1)
    t.sleep(2)
    LC=open(list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    Q_logger(fnames1,variable2)
    print "priority list is %s"%fnames1
    if fnames1==[]:
        print "priority List is empty"
        list_creator_normal(normal_loc,'Normal')
    else :
        main_prog(fnames1[0],priority_loc)

#List Creator for small runs. Checks file Size before proceeding..        
def list_creator_smallruns(variable1, variable2):
    print"variable 1 is %s"%variable1
    list_name='List_%s.txt'%variable2
    list_loc=os.path.join(admin_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_CL2.BAT')
    print variableA1
    BC=open('%s'%variableA1,'w')
    BC.write('@Echo off\ncd /d " "%s"\ndir *.def /OD /b /s >"%s"'%(variable1,list_loc))
    BC.close()
    t.sleep(2)
    os.popen('"%s"'%variableA1)
    t.sleep(2)
    LC=open(list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    Q_logger(fnames1,variable2)
    print "Small runs priority list is %s"%fnames1
    if fnames1==[]:
        print "Small runs priority List is empty. Going to Priority"
        list_creator_priority(priority_loc,'Priority')
    else :
        if (os.stat("%s"%fnames1[0]).st_size<180000000):
            print "Small run file size is okay. Processing..."
            main_prog(fnames1[0], small_runs_loc)            
        else :
            print "Small Run File Size is Excess. Moving out.."            
            move_command(fnames1[0], excess_size_loc, small_runs_loc)
            print "Exiting.."
            t.sleep(1)
            print "Deleting Scan flag"        
            flag_del('CL2_scan.txt')
            exit()
  from random import choice, randint
    
## Beat poetry

adjectives = "radiant bright ecstatic young lithe driving running splitting".split()
verbs = "wriggles grows stares saunters drives smiles raps".split()
nouns = "pen inkwell willow sky station train pane window sunlight dust".split()

def beat_poem():
    print "\n" + "="*16+" a poem " + "="*16
    for x in range(randint(5,11)):
        words1 = " ".join([choice(adjectives) + ", ", choice(adjectives)])
        words2 = " ".join([choice(nouns), choice(verbs)])
        words3 = " ".join([choice(nouns), choice(nouns), choice(adjectives), choice(nouns)])
        
        for i in range(randint(2,5)):
            words = choice([words1, words2, words3])
            line = " "*randint(0, 40 - len(words)) + words
            print line
        
        if x % 3 ==0:
            print
            print " "*5 + choice(nouns)
            print " "*5 + choice(nouns)
            print " "*5 + "the " + choice(nouns) +"!"
            print
        
        if x % 7 ==0:
            words4 = " ".join(["the " + choice(adjectives), choice(nouns), choice(verbs)])
            print
            print " ".join(words4)
            print
beat_poem()
#List Creator for Long Status Runs. Runs only if Small runs, priority and normal lists are empty.
def list_creator_long(variable1, variable2):
    print"variable 1 is %s"%variable1
    list_name='List_%s.txt'%variable2
    list_loc=os.path.join(admin_loc,list_name)
    variableA1=os.path.join(variable1,'list_creator_CL2.BAT')
    print variableA1
    BC=open('%s'%variableA1,'w')
    BC.write('@Echo off\ncd /d " "%s"\ndir *.def /OD /b /s >"%s"'%(variable1,list_loc))
    BC.close()
    t.sleep(2)
    os.popen('"%s"'%variableA1)
    t.sleep(2)
    LC=open(list_loc,'r')
    fnames1=LC.read().splitlines()
    LC.close()
    Q_logger(fnames1,variable2)
    print "Long status list is %s"%fnames1
    if fnames1==[]:
        print "Long List is empty"
        print "Deleting Scan flag"        
        flag_del('CL2_scan.txt')
        exit()
    else :
        main_prog(fnames1[0],long_loc)

          
#Reading the list generated and passing the first def file to the main program.
def list_reader(variable1):
    f = open("%s"%(fdiff_loc),'r')
    fnames1 = f.read().splitlines()
    f.close()
    main_prog(fnames1[0])

#Function for deleting the older BAT files used to execute the simulation. Prevents Clutter.
def BAT_killer(variable):
    for variable in glob.glob('%s/*_CL2.BAT'%variable):
        if os.path.isfile(variable):
            os.remove(variable)
            
#Function for scanning if other cluster is scanning. Prevents Race condition.
def Scan_race(variable,var2):
    for variable in glob.glob('%s/%s_scan.txt'%(variable,var2)):
        if os.path.isfile(variable):
            print "Race exists. Pausing for 25 secs"
            t.sleep(22)
            #exit()

#Creating and deleting Flag for showing the simulation is running.
def flag_create(variable):
    print "Creating the Flag for simulation run"
    stat_loc=os.path.join(admin_loc,variable)
    f=open(stat_loc,'w')
    f.write("Running")
    f.close()

def flag_del(variable):
    print "Deleting the Flag for simulation run"
    stat_loc=os.path.join(admin_loc,variable)
    os.remove(stat_loc)

#Main Program - gets variable (Def file name) from Priority first and if empty, from Normal
def main_prog(variable,v2):
    BAT_killer(simworking_loc)
    loc1='"%s"'%variable
    loc2='"%s"'%simworking_loc
    temp1=os.path.split(variable)
    runner_name=os.path.join(simworking_loc,temp1[1])
    move_command(loc1,loc2,v2)
    print "\n\nFinished Moving files"
    flag_del('CL2_scan.txt')
    flag_create('status2.txt')
    R_logger(variable)
    run_exec(runner_name)
    t.sleep(1)
    flag_del('status2.txt')
    BAT_killer(simworking_loc)
    temp2=os.path.splitext(temp1[1])[0]
    success_scan(simworking_loc,temp2,'res')
    if success_scan.scanperm=='yes':
        success_scan(simworking_loc,temp2,'out')
        success_scan(simworking_loc,temp2,'def')
    else: print "Since Res file unavailable. Leaving def and out file in working_loc..."

#Scans for res file matching the def file name and then an out file.
#If available, the res,def and out files are transfered to the completed folder.  
#If res file unavailable, def and out files remain in working_loc
def success_scan(variable1, variable2, variable3):
    p2=glob.glob('%s/%s*.%s' %(variable1,variable2, variable3))
    #print p2
    if p2==[]:
        print "No %s file..."%variable3
        success_scan.scanperm='no'
        return success_scan.scanperm
    else:
        success_scan.scanperm='yes'        
        print "the matching %s file is %s" %(variable3,p2[0])
        move_command(p2[0],completed_loc,variable1)
        return success_scan.scanperm

#Program first checks if the Pause flag is up. If yes - program exits. 
#If No - program checks if the Run Flag is up or down. If down - moves to Priority list creation. If Up - Program exits.
fexist1=os.path.isfile('%s'%pause_set_loc)
print "Pause Status Set ?%s" %fexist1
if (fexist1==True):
    print "Pause for CL 2 Request available. Exiting program"
    exit()
else:
    print "Pause for CL2 setting is Off. Checking Run Status.."
    
fexist2=os.path.isfile('%s'%status_loc)
print "Status 2 File Exists? %s" %fexist2
#print "Checking for Single Cluster Mode and Cluster 1 status"
fexist3=os.path.isfile('%s'%single_cl_mode_loc)
fexist4=os.path.isfile('%s'%status_other_loc)
if (fexist2==True):
    print "Exiting program as status is active."
    exit()
else:
    print "Good to go. Creating Current Scan Flag.."
    t.sleep(5)
    flag_create('CL2_scan.txt')
    print "Checking for Race Condition..."
    Scan_race(admin_loc,'CL1')
    print "Run can start. Going to the Small Runs Priority folder..."
    list_creator_smallruns(small_runs_loc,'Small Run Priority')
