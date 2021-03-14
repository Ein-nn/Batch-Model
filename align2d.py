from modeller import *

env = environ()
aln = alignment(env)
mdl = model(env, file='aaaa', model_segment=('FIRST:A','LAST:A'))
aln.append_model(mdl, align_codes='aaaaA', atom_files='aaaa.pdb')
aln.append(file='0000.ali', align_codes='0000')
aln.align2d()
aln.write(file='0000-aaaaA.ali', alignment_format='PIR')
aln.write(file='0000-aaaaA.pap', alignment_format='PAP')
