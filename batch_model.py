# -*- coding: utf-8 -*-
# @Author: Hangyang Zhang
# @Date:   2020-07-18 10:10:16
# @Last Modified by:   Ein
# @Last Modified time: 2020-08-06 18:25:36

import os
import re
import time
import shutil
import requests
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML

fastafile = "transpoter.fasta"

# # read ids of tempalte matching to sequences
# temp = {} # dictionary of templates
# with open("template_id.txt") as f:
#     for line in f.readlines():
#         ids = line.strip().split("\t")
#         temp[ids[0]] = ids[1]

# split fasta file into single sequence
seqs = [] # sequences of proteins
with open(fastafile) as f:
    lines =  f.readlines()
    i = 0
    while i < (len(lines)-1):
        seqs.append([lines[i].strip().replace('>CCM_0',''),lines[i+1].strip()])
        i += 2

# excute the command lines of mod to model
def model(seq_id):
    with open('mod_pattern.bat') as f:
        with open('mod.bat', 'w') as m:
            m.write(re.sub(r'0000', seq_id, f.read()))
    # open('mod.bat', 'w').write(re.sub(r'0000', seq_id, open('mod_pattern.bat').read()))
    os.system("cmd /c \"mod.bat\"")

# blast on line using Biopython to search templates and return the pdb id of the template with chain id
def blast_template(seq_id, seq_seq):
    try:
        result_handle = NCBIWWW.qblast("blastp", "pdb", seq_seq)
        data = result_handle.read()
    except Exception as e:
        data = e.partial
    # save results as a xml file
    save_file = open(seq_id+"/blast.xml", "w")
    # save_file.write(result_handle.read())
    save_file.write(data)
    save_file.close()
    result_handle.close()
    # filter results of blast
    result_handle = open(seq_id+"/blast.xml")
    blast_record = NCBIXML.read(result_handle)
    result_handle.close()
    hits = blast_record.alignments
    if len(hits) == 0:
        return "****"
    else:
        temp_id = hits[0].accession
        cover = hits[0].hsps[0].align_length/blast_record.query_length
        ident = hits[0].hsps[0].identities/hits[0].hsps[0].align_length
        if cover > 0.5 and ident > 0.2:
            t.write(seq[0] +"\t"+ temp_id +"\t"+ str(cover) +"\t"+ str(ident) + "\n")
            return temp_id
        else:
            return "****"

# download the pdb file of tempalte form PDB and modify format
def get_pdb(seq_id,pdb_id):
    url = "http://files.rcsb.org/download/aaaa.pdb".replace("aaaa",pdb_id)
    r = requests.get(url)
    # pdb = re.sub(r'^HETATM.+$\n','',bytes.decode(r.content))
    with open(seq_id+"/"+pdb_id+".pdb", "wb") as code:
        code.write(r.content)

# Version 2 -- automatically search templates by Biopython +++++++++++++++++++++++++++
t = open("templates_information.txt", "w")
# call function to model one by one
for seq in seqs:
    # creat folder each of which contains the unique ali, py and pdb files
    os.makedirs(seq[0])
    # save sequence to ali format
    with open(seq[0]+"/"+seq[0]+".ali","w") as f:
        f.write(">P1;"+seq[0]+"\nsequence:"+seq[0]+":::::::0.00: 0.00n\n"+seq[1])
    
    temp_id = blast_template(seq[0],seq[1])
    if temp_id == "****":
        t.write(seq[0] +"\t****\n")
        time.sleep(1)
    else:
        temp =temp_id.split("_")
        get_pdb(seq[0], temp[0])
        # modify py files of mod to adapt to different ids
        with open("align2d.py") as f:
            with open(seq[0]+"/"+"align2d.py","w") as m:
                # m.write(re.sub(r'aaaa', temp[seq[0]], re.sub(r'0000', seq[0], f.read())))
                m.write(re.sub(r':A', ":"+temp[1], re.sub(r'aaaa', temp[0], re.sub(r'0000', seq[0], f.read()))))
        with open("mod-single.py") as f:
            with open(seq[0]+"/"+"mod-single.py","w") as m:
                m.write(re.sub(r'aaaaA', temp[0]+temp[1], re.sub(r'0000', seq[0], f.read())))
        # template_path = "templates/"+temp[0]+".pdb"
        # template_new_path = template_path.replace("templates", seq[0])
        # shutil.move(template_path, template_new_path)
        model(seq[0])

t.close()
# # Version 1 -- manually search templates by hand ++++++++++++++++++++++++++++++++++++
# # call function to model one by one
# for seq in seqs:
#     # creat folder each of which contain the unique ali, py and pdb files
#     os.makedirs(seq[0])
#     # save sequence to ali format
#     with open(seq[0]+"/"+seq[0]+".ali","w") as f:
#         f.write(">P1;"+seq[0]+"\nsequence:"+seq[0]+":::::::0.00: 0.00n\n"+seq[1])
#     # modify py files of mod to adapt to different ids
#     with open("align2d.py") as f:
#         with open(seq[0]+"/"+"align2d.py","w") as m:
#             m.write(re.sub(r'aaaa', temp[seq[0]], re.sub(r'0000', seq[0], f.read())))
#     with open("mod-single.py") as f:
#         with open(seq[0]+"/"+"mod-single.py","w") as m:
#             m.write(re.sub(r'aaaa', temp[seq[0]], re.sub(r'0000', seq[0], f.read())))
#     template_path = "templates/"+temp[seq[0]]+".pdb"
#     template_new_path = template_path.replace("templates", seq[0])
#     shutil.move(template_path, template_new_path)
#     model(seq[0])
