import subprocess
import argparse
import math
import os
import re

from collections import namedtuple

HausdorffDistance = namedtuple('HausdorffDistance', ['fileA', 'fileB', 'nptsA', 'dmin', 'dmax', 'dmean', 'dRMS'], verbose=False)

def hausdorff_distance_one_direction(mesh1_filepath, mesh2_filepath):
    mlx_path = os.path.abspath(__file__).replace(__file__, "distance.mlx")
    f = open(os.devnull, 'w')
    cmd_str = "meshlabserver -s " + mlx_path + " -i " + mesh1_filepath + " " + mesh2_filepath
    output = subprocess.check_output(cmd_str.split(" "), stderr=f)
    result = output.split("\n")
    # parse result to get values                                                                                                                                                                         
    data = ""
    num_pnts1 = 0
    
    for idx, line in enumerate(result):
        m = re.match(r"\s*Sampled (\d+) pts.*", line)
        if m is not None:
            num_pnts1 = int(m.group(1))
        if line == 'Hausdorff Distance computed':
            data = result[idx+2]
    m = re.match(r"\D+(\d+\.*\d*)\D+(\d+\.*\d*)\D+(\d+\.*\d*)\D+(\d+\.*\d*)", data)
    min_distance = float(m.group(1))
    max_distance = float(m.group(2))
    mean_distance = float(m.group(3))
    RMS_distance = float(m.group(4))

    return HausdorffDistance(fileA=mesh1_filepath, 
                             fileB=mesh2_filepath,
                             nptsA=num_pnts1,
                             dmin=min_distance,
                             dmax=max_distance,
                             dmean=mean_distance,
                             dRMS=RMS_distance)

def hausdorff_distance(mesh1_filepath, mesh2_filepath):
    # get hausdorff dist from meshlab server                                                                                                                                                                
    hd_ab = hausdorff_distance_one_direction(mesh1_filepath, mesh2_filepath)
    hd_ba = hausdorff_distance_one_direction(mesh2_filepath, mesh1_filepath)

    min_BI = min(hd_ab.dmin, hd_ba.dmin)
    max_BI = max(hd_ab.dmax, hd_ba.dmax)
    
    sm = hd_ab.dmean*hd_ab.nptsA + hd_ba.dmean*hd_ba.nptsA
    mean_BI = sm / (hd_ab.nptsA + hd_ba.nptsA)

    ms = (hd_ab.dRMS**2)*hd_ab.nptsA + (hd_ba.dRMS**2)*hd_ba.nptsA
    RMS_BI = math.sqrt(ms/(hd_ab.nptsA+hd_ba.nptsA))

    return HausdorffDistance(fileA=mesh1_filepath, 
                             fileB=mesh2_filepath,
                             nptsA=hd_ab.nptsA,
                             dmin=min_BI,
                             dmax=max_BI,
                             dmean=mean_BI,
                             dRMS=RMS_BI)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Compute Hausdorff Distance Between Two Meshes')
    parser.add_argument('mesh_filepaths', metavar='N', type=str, nargs='+',
                    help='meshes to compare')

    args = parser.parse_args()

    mesh_files = args.mesh_filepaths
    
    if len(mesh_files) != 2:
        print "wrong number of mesh files: wanted 2, got: " + str(len(mesh_files))

    dist = hausdorff_distance(mesh_files[0], mesh_files[1])
    
    print dist

    

 
 
