import jinja2
from jinja2 import Environment, FileSystemLoader, Template
import os

###############################################
# Library to create automatically inputs for  #
# first principle calculations in gfnxtb       #
###############################################

def cluster_script(user,queue,project,walltime,cpus,nodes,mem):
  """ Creating the header of the submit.sh
      for launching the gfnxtb calculations 
      in the cluster 
  """ 
  cluster_script = """#!/bin/sh
#PBS -N {{ user }}
#PBS -q {{ queue }}
#PBS -P {{ project }}
#PBS -l walltime={{ walltime }}
#PBS -l select={{ nodes }}:ncpus={{cpus}}:mem={{mem}}gb
  """
  return Environment().from_string(cluster_script).render(user=user,project=project,queue=queue,walltime=walltime,nodes=nodes,cpus=cpus,mem=mem)


def cluster_xtb_options(path,num_threads,mkl_threads,stack_size,path_2,path_3):
   """ Block of the dftb input activating the eigensolver and differentation options
   """
   cluster_xtb_options="""export XTB={{path}} 
export OMP_NUM_THREADS={{ num_threads }} 
export MKL_NUM_THREADS={{ mkl_threads }}
export OMP_STACKSIZE={{ stack_size }}m
export XTBPATH={{path_2}}
export XTBHOME={{path_3}}
   """
   return Environment().from_string(cluster_xtb_options).render(path=path, num_threads=num_threads,mkl_threads=mkl_threads,stack_size=stack_size,path_2=path_2,path_3=path_3)

def gfnxtb_sp(path,coord,num_cores):
   """ gfnxtb command to optimize the structure 
   """
   gfnxtb_opt="""{{path}} {{coord}} --scc --parallel {{num_cores}}
   """
   return Environment().from_string(gfnxtb_opt).render(path=path,coord=coord,num_cores=num_cores)
 
def gfnxtb_opt(path,coord,num_cores):
   """ gfnxtb command to optimize the structure 
   """
   gfnxtb_opt="""{{path}} {{coord}} --opt --parallel {{num_cores}}
   """
   return Environment().from_string(gfnxtb_opt).render(path=path,coord=coord,num_cores=num_cores)

def gfnxtb_hess(path,coord,num_cores):
   """ gfnxtb command to compute only the hessian
   """
   gfnxtb_hess="""{{path}} {{coord}} --hess --parallel {{num_cores}}
   """
   return Environment().from_string(gfnxtb_hess).render(path=path,coord=coord,num_cores=num_cores)

def gfnxtb_vip(path,coord,num_cores):
   """ gfnxtb command to compute the ionization potential (IP)
   """
   gfnxtb_ip="""{{path}} {{coord}} --vip --parallel {{num_cores}}
   """
   return Environment().from_string(gfnxtb_ip).render(path=path,coord=coord,num_cores=num_cores)

def gfnxtb_vea(path,coord,num_cores):
   """ gfnxtb command to compute the electron affinity (EA)
   """
   gfnxtb_ea="""{{path}} {{coord}} --vea --parallel {{num_cores}}
   """
   return Environment().from_string(gfnxtb_ea).render(path=path,coord=coord,num_cores=num_cores)

def gfnxtb_md(path,coord,temp,num_cores):
   """ gfnxtb command to compute Md calculations
   """
   gfnxtb_ohess="""{{path}} {{coord}} --md --parallel {{num_cores}}
   """
   return Environment().from_string(gfnxtb_ohess).render(path=path,coord=coord,temp=temp,num_cores=num_cores)
 
# Test to print the different blocks of the input
if __name__ == '__main__':
#    print(cluster_script("asanta","general","try_1","try_2","1","1","1"))
#    print (cluster_xtb_options("la","la","la","la","la","la"))
    print(gfnxtb_opt("/home/santaninci/gfnxtb_creator/", "mol.xyz", "4"))

