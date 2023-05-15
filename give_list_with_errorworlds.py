import os
from glob import glob

def get_error_launchfile_list(bagfiles):
    l = []
    for bag in bagfiles:
        if "error" in bag:
            l.append(os.path.basename(bag).split(".launch")[0]+".launch")
    return l

def write_bash_if_condition(error_bags,outdir="/home/linux123/Dokumente"):
    with open(os.path.join(outdir,"error_if.txt"),"w") as file:
        for i,bag in enumerate(error_bags):
            line = "	 		if " if i == 0 else "				"
            line += f'[ $launchfile != "{bag}" ]'
            if i != len(error_bags): line+= " && \\\n"
            file.write(line)

if __name__ == "__main__":
    workdir = "/home/linux123/bagfiles_all_worlds"
    bagfiles = glob(os.path.join(workdir, "*.bag"))
    write_bash_if_condition(get_error_launchfile_list(bagfiles))
