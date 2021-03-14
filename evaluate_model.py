from modeller import *
from modeller.scripts import complete_pdb
log.verbose()    # request verbose output
env = environ()
env.libs.topology.read(file='$(LIB)/top_heav.lib') # read topology
env.libs.parameters.read(file='$(LIB)/par.lib') # read parameters
mdl = complete_pdb(env, 'TMC6.B99990003.pdb')
s = selection(mdl)
s.assess_dope(output='ENERGY_PROFILE NO_REPORT', file='TMC6_mu_03.profile',
              normalize_profile=True, smoothing_window=15)
