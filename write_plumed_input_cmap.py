def write_plumed_input_rational_d0(native_contacts, reference_distances,name="NMR"):
    """Function that formats plumed based input contacts for rational switch with d0 != 0.
    
    Parameters
    ----------
    native_contatcs: list
        contains the contact that you want to include in the CV
    reference_distances: list
        distances between the contact partners in the reference/starting structure in nm.
    Writes
    ------
    file: txt file
        plumed contact map
    """
    
    file = open(folder + "/cmap_rat_{}.txt".format(name), "w")
    file.write("CONTACTMAP ...\n")
    for m in range( len( native_contacts )):
        i, j = native_contacts[m]
        file.write("ATOMS{m}={i},{j} SWITCH{m}={{RATIONAL R_0=0.3 D_0={dist:.4f} }}\n"\
                   .format(i=i+1,j=j+1,m=m+1, dist = reference_distances[m]))
    file.write("LABEL=cmap\n")
    file.write("SUM\n")
    file.write("... CONTACTMAP\n")
    file.close()
