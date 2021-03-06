import glob, iotbx.pdb, os, time
from libtbx import easy_run
from subprocess import check_output
import shutil

def file_size(fname):
    statinfo = os.stat(fname)
    return statinfo.st_size
############### end of file_size()


def check_whether_the_step_was_successfully_ran_in_regression(step_name, check_this_file):
  if (os.path.isfile(check_this_file)):
    returned_file_size = file_size(check_this_file)
    if (returned_file_size > 0):
      #if (step_name != "Step 8"): # for step_8 (drawing a graph), determining a success now is early
      #  print step_name, " successfully ran"
      return 1
  print step_name, " didn't successfully ran"
  return 0
####################### end of check_whether_the_step_was_successfully_ran_in_regression function


def run():
    """
    Exercise phenix.cryo_fit with all defaults with the small dataset"
    """
    
    assert (os.path.isfile("data/regression_pdb5khe_10_AA.ccp4") == True)
    assert (os.path.isfile("data/regression_pdb5khe_10_AA.pdb") == True)
  
    # to avoid 322122547200 steps !!!!!!!
    if (os.path.isfile("aim_this_step_when_restart.txt") == True):
        cmd = "rm aim_this_step_when_restart.txt"
        easy_run.call(cmd)
    
    #"Fatal error: Step 9360: The domain decomposition grid has shifted too much in the Y-direction around cell 1 1 0"
    '''cmd = " ".join([
      "phenix.cryo_fit",
      "data/regression_pdb5khe_10_AA.pdb",
      "data/regression_pdb5khe_10_AA.ccp4"
      ])
    '''
      
    cmd = " ".join([
      "phenix.cryo_fit",
      "data/regression_pdb5khe_10_AA.pdb",
      "data/regression_pdb5khe_10_AA.ccp4",
      'nproc=2'
      ])
      
    print cmd
    easy_run.call(cmd)
  
    starting_dir = os.getcwd()
    new_path = starting_dir + "/output"
    if (os.path.exists(new_path) == False):
        print "regression with regression_pdb5khe.pdb with restart"
        print "failed, sleep for 10,000 seconds"
        time.sleep(10000) # so that it is recognized instantly
        exit(1)
    
    os.chdir( new_path )
    
    the_step_was_successfully_ran = ''
    for gro in glob.glob("*.gro"):
      the_step_was_successfully_ran = check_whether_the_step_was_successfully_ran_in_regression("Step final", gro)
      break
    
    if (the_step_was_successfully_ran != 1):
        print "failed, sleep for 10,000 seconds"
        time.sleep(10000) # so that it is recognized instantly
    assert (the_step_was_successfully_ran != 0)
    
    os.chdir(starting_dir)
    shutil.rmtree("output")
    shutil.rmtree("steps")
    
    if (os.path.isfile("aim_this_step_when_restart.txt") == True):
        os.remove("aim_this_step_when_restart.txt")
    
############ end of run()

if (__name__ == "__main__"):
  t0=time.time()
  returned = run()
  print "Time: %6.4f"%(time.time()-t0) #on Doonam's lanl 13inch laptop, it took 2 seconds
  print "OK"

