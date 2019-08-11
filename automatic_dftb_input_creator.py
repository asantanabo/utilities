import jinja2
from jinja2 import Environment, FileSystemLoader, Template
import os

###############################################
# Library to create automatically inputs for  #
# first principle calculations in DFTB+       #
###############################################

def dftb_geom(name):
  """ Creating the header of the DFTB input file
  where the geometry name must be specified. The 
  user must provide the name of the file and is
  expected to be transformed to the .gen format 
  """ 
  dftb_geom = """Geometry = GenFormat {
  <<< "{{ title }}"
  }
  """
  return Environment().from_string(dftb_geom).render(title=name)

def dftb_driver(relax_method, atoms_rel, thres_force, num_steps):
    """ Block of the input file in which the user decides
        the relaxation method, atoms to be relaxed, threshold of force 
        and number of steps. For more detailed options refer to 
        the dftb manual. 
    """
    dftb_driver= """Driver = {{ relax_method }} {
    MovedAtoms = {{ atoms_rel }}
    MaxForceComponent = {{ thres_force }}
    MaxSteps = {{ num_steps }}
    }
    """
    return Environment().from_string(dftb_driver).render(relax_method=relax_method,atoms_rel=atoms_rel,thres_force=thres_force,num_steps=num_steps)

def dftb_hessian(num_atoms, tol):
  """Block of the input file that activates the computation of the 
     second derivatives for the studied system in DFTB+ 
  """
  dftb_hessian="""Driver = SecondDerivatives{
   Atoms = {{ num_atoms }}
   Delta = {{ tol }}
   }
  """
  return Environment().from_string(dftb_hessian).render(num_atoms=num_atoms,tol=tol)

def dftb_hamil_1(scc,ssc_tol,max_iter,mix_param):
    """ First Block of the Hamiltonian section of DFTB+
        to activate the SCC calculations and options related to it.
        Please look the manual for reference of each option.
    """
    dftb_hamil_1="""Hamiltonian = DFTB{
     SCC = {{ scc }}
     SCCTolerance = {{ ssc_tol }}
     MaxSCCIterations = {{ max_iter }}
     Mixer = Broyden {
     MixingParameter = {{ mix_param }}
    }
    """
    return Environment().from_string(dftb_hamil_1).render(scc=scc,ssc_tol=ssc_tol,max_iter=max_iter,mix_param=mix_param)

def dftb_hamil_2(path_slako):
    """ Block of the Hamiltonian section where to locate the slako files (.skf)
    """
    dftb_hamil_2 = """
    SlaterKosterFiles = type2filenames {
    prefix = "{{  path_slako  }}"
    separator = "-"
    suffix = ".skf"
    }
    """
    return Environment().from_string(dftb_hamil_2).render(path_slako=path_slako)

def dftb_hamil_3(elements):
    """ DFTB block to write the Angular momentum of the different elements that is provided by the 
        user as an array "elements". The information is organized in a dictionary and then organized
        in an array to create the template. This template is correspondingly changed.  
    """
    dftb_ang_momentum = {
      "Br" : "Br = d", "C": "C = p", "Ca" : "Ca = p", "Cl": "Cl = d",
      "F": "F = p", "H": "H = s", "I": "I = d", "K": "K = p", "Mg": "Mg = p",
      "N": "N = p", "Na" : "Na = p", "O": "O = p", "P": "P = d", "S": "S = d",
      "Zn": "Zn = d" }
    
    species = []
    for i in range(len(elements)):
      species.append(dftb_ang_momentum[elements[i]]) 

    mytemplate = Template("""
    MaxAngularMomentum {
      {% for item in numbers %}{{ item }}
      {% endfor %}
    }""")
    return(mytemplate.render(numbers=species))
      
def dftb_filling_fermi(unit, elec_temp):
   """ Block in DFTB+ input to activate electronic temperature according to the Fermi distribution
   """
   dftb_filling_fermi = """
   Filling =  Fermi {
    Temperature [{{ unit }}] = {{ elec_temp }}
   }
   """
   return Environment().from_string(dftb_filling_fermi).render(unit=unit, elec_temp=elec_temp)

def dftb_filling_mp(order):
   """ Activate electronic temperature according to the MethfesselPaxton distribution
   """
   dftb_filling_fermi = """
   Filling = MethfesselPaxton{
     Temperature [{{ unit }}] = {{ elec_temp }}
     order = {{ order }}
   }
   """
   return Environment().from_string(dftb_filling_fermi).render(unit=unit, elec_temp=elec_temp)

def dftb_hamil_4(eig_solver, diff):
   """ Block of the dftb input activating the eigensolver and differentation options
   """
   dftb_hamil_4="""
   Eigensolver = {{eig_solver}} {}
   Differentiation = {{ diff }} {}
   """
   return Environment().from_string(dftb_hamil_4).render(eig_solver=eig_solver, diff=diff)


def dftb_dftd3(third_ord, damp_flag, damp_exp):
   """ Block of the DFTB input to activate the use of the DFTB-D3 approach 
   """
   dftb_dftd3="""
   ThirdOrderFull = {{  third_ord }}
   DampXH = {{  damp_flag }}
   DampXHExponent = {{  damp_exp }}
   Dispersion = DftD3{}
}
      """
   return Environment().from_string(dftb_dftd3).render(third_ord=third_ord, damp_flag=damp_flag, damp_exp=damp_exp)

def dftb_parser(level):
     """DFTB+ parser block. Currently the parsel 5 level is the standard
        and needed for utilizing the code.
     """
     dftb_parser="""ParserOptions {
      ParserVersion = {{  level  }}
      }
     """
     return Environment().from_string(dftb_parser).render(level=level)
   
 
# Test to print the different blocks of the input
if __name__ == '__main__':

    print(dftb_geom("mol.gen"))
    print(dftb_driver("ConjugateGradient", "1:-1", "1E-8", "10"))
    print(dftb_hamil_1("Yes","10E-10","100","0.99"))
    print(dftb_hamil_2("/home/santaninci/Documents/calculations/dftb/slako/3ob-3-1/"))
    print(dftb_hamil_3(['C','O','H']))
    print(dftb_filling_fermi("Kelvin", "1000"))
    print(dftb_hamil_4("DivideAndConquer","Richardson"))
    print(dftb_dftd3("Yes","Yes","4.0"))
    print(dftb_parser("5"))
