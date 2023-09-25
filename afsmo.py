import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from scipy.interpolate import interp1d

template ="""\
{airfoil_title}
{max_iter:10.5f}  10.00000{ipunch:10.5f}   0.00000{icamtk:10.5f}{ibad:10.5f}{itrn:10.5f}   2.00000 
{n_upper}
{xy_upper}
{n_lower}
{xy_lower}
{n_inter}
{x_inter} 
  1.         
"""

def clear_dir():
    """
    Clear the output files from the previous run if exists
    """
    files_to_be_removed = ["afsmo.out","afsmo.pch","afsmo.dat","afsmo.smr"]
    for file in files_to_be_removed:
        if os.path.exists(file):
            os.remove(file)

def extract_afsmo_dat(filename="afsmo.dat"):
    """
    Reads the xy dump file created by AFSMO and spits out
    the coordinates in standard *.dat format
    """
    x, y= np.loadtxt(filename).T
    split_idx = np.argmax(x)+1 # First 1.000.. index of the x array -- end of upper surface
    x_upper = x[:split_idx][::-1]
    y_upper = y[:split_idx][::-1]
    x_lower = x[split_idx:][1:]
    y_lower = y[split_idx:][1:]
    return np.concatenate([x_upper,x_lower]), np.concatenate([y_upper,y_lower])

def extract_datfile_title(filename):
    """
    Reads title and x,y data from a standard *.dat file 
    """
    title = open(filename).readlines()[0].strip()
    return title

def extract_datfile_data(filename):
    """
    returns x,y point array extracted from a standard XFoil *.dat file. 
    """
    return np.loadtxt(filename, skiprows=1)

def gen_input(title, x,y, input_filename, **kwargs):
    """
    Creates an input file for AFSMO. 
    Standard *dat file x,y array is split from the LE to create 4 arrays on Upper and Lower XY data.
    Fixed number of Interpolation points were created with cosine spacing with maximum possible (100)
    Once data is generated it will be dumped in to a standard template. (template.in file)
    """
    le = x.argmin()

    xu = x[:le+1][::-1]
    yu = y[:le+1][::-1]

    xl = x[le:]
    yl = y[le:]

    nu = len(xu)
    nl = len(xl)

    xy_upper = "\n".join("{:12.6f}{:12.6f}".format(x,y) for x,y in zip(xu,yu))
    xy_lower = "\n".join("{:12.6f}{:12.6f}".format(x,y) for x,y in zip(xl,yl))

    x_inter = 0.5*(1 + np.cos(np.linspace(np.pi, 0, 100)))
    x_inter = "\n".join(["{:12.6f}".format(x) for x in x_inter])

    file_content = template.format(airfoil_title= title, 
                                   n_upper      = nu, 
                                   xy_upper     = xy_upper, 
                                   n_lower      = nl, 
                                   xy_lower     = xy_lower, 
                                   n_inter      = 100, 
                                   x_inter      = x_inter,
                                   **kwargs)
    with open(input_filename, "w") as f:
        f.write(file_content)

def write2dat(title, x_new, y_new, filename):
    """
    Writes xy data in to an airfoil *.dat file
    To keep the precision :.7f format was used.
    """
    data = "\n".join(["{:.7f} {:.7f}".format(x,y) for x,y in zip(x_new, y_new)])
    with open(filename, "w") as f:
        f.write("{}\n{}".format(title,data))

def extract_afsmo_smr(filename="afsmo.smr"):
    """
    Reads the summary dump file created by AFSMO and spits out
    the x,y and y_smoothed coordinates. Helpful in identifying how successful the 
    smoothing process was, without interpolation
    """
    theta, x, y_smoo = np.loadtxt(filename, skiprows=5, usecols=(1,2,5)).T
    return theta, x, y_smoo

def interpolate_new_points(theta, x, y, n_inter):
    # New point generation through interpolation is now done through python

    theta_x_spline = interp1d(theta,x, kind='cubic', fill_value='extrapolate')
    theta_y_spline = interp1d(theta,y, kind='cubic', fill_value='extrapolate')

    # Theta goes from 180 to -180 such that the points are laid out counter-clockwise
    new_theta = np.linspace(180, -180, n_inter)

    # new_theta = np.concatenate((new_theta[new_theta<0], [0], new_theta[new_theta>0]))
    # Adding 0 above is a bad idea. MSS proved the curvature discontinuity through Rhino
    # Keeping this commented out in case I forget in the future.

    new_x = theta_x_spline(new_theta)
    new_y = theta_y_spline(new_theta)

    return new_x, new_y


def plot(x,y, x_new, y_new, title, aspect_equal=False):
    """
    plots original and smoothed airfoil coordinates for comparison
    """
    plt.title(title)
    plt.plot(x, y, lw=0.5, color='blue', label="Original")
    plt.plot(x_new, y_new, lw=0.5, color='red', label="Smoothed")
    plt.legend()
    if aspect_equal:
        plt.gca().set_aspect("equal", 'datalim')
    plt.show()

def afsmo(dat_file, interpolate, n_inter, plotter, aspect_equal, **kwargs):
    """
    main program
    1. extracts data from standard dat file
    2. Generates an *.in file understandable by AFSMO
    3. Runs AFSMO
    4. Extract data from AFSMO output file
    5. Rearranges the extracted data applicable for *dat files
    6. Writes smoothed coordinates to a dat file
    7. Plots both airfoils for comparison
    """
    clear_dir()

    # setup file names and airfoil title
    dat_basefilename = dat_file[:-4]
    in_file = "{}.in".format(dat_basefilename)
    out_file = dat_basefilename + "_sm.dat"
    title = extract_datfile_title(dat_file)

    x, y  = extract_datfile_data(dat_file).T
    
    gen_input(title, x,y, in_file, **kwargs)
    os.system("{} {}".format("afsmo.exe" if os.name == "nt" else "./afsmo", in_file))
    
    try:
        theta, x_new, y_new  = extract_afsmo_smr()
        theta = theta[::-1]
        x_new = x_new[::-1]
        y_new = y_new[::-1]
        if interpolate:
            x_new, y_new = interpolate_new_points(theta, x_new, y_new, n_inter)    
    except:
        print("Failure encountered")
        return

    write2dat(title, x_new, y_new, out_file)
    write2dat(title, *extract_afsmo_dat(), 'afsmo.dat')

    if plotter:
        plot(x,y, x_new, y_new, title, aspect_equal)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple wrapper for NASA AFSMO airfoil smoothing program',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-d', '--dat-file',    
                        metavar='',
                        type=str,  
                        help='Input *.dat file name')

    parser.add_argument('-i', '--interpolate',
                        help="Dat file with (n) interpolated x coordinates will be generated when set\nDefault => True\n",
                        action='store_true')

    parser.add_argument('-n', '--n-inter',    
                        metavar='',
                        type=int,  
                        help='Number of cosine spaced points to be interpolated\nDefault =>  160\n', 
                        default=160)

    parser.add_argument('-p', '--plotter',    
                        help='Plots the original and Smoothed airfoils\nDefault => True\n', 
                        action='store_true')

    parser.add_argument('-a', '--aspect',     
                        help='Uses real aspect ratio for plotting\nDefault => True\n', 
                        action='store_true')

    adopts = parser.add_argument_group('Advanced options')

    adopts.add_argument('--max-iter',    
                        metavar='',
                        type=int,  
                        help='MAXIMUM NUMBER OF SMOOTHING ITERATIONS\n        DEFAULT =>80\n'.title(), 
                        default=80)

    adopts.add_argument('--ipunch',    
                        metavar='',
                        type=int,  
                        help="""\
IPUNCH - PUNCH OUTPUT OPTION                        
    0 - NO PUNCHED OUTPUT                      
    1 - SMOOTHED (X,Y,W) PUNCHED               
    2 - SMOOTHED (THETA,Y/C,W) PUNCHED         
    3 - SMOOTHED (THETA,YPS,W) PUNCHED 
        (YLTE, YNOSE, AND YUTE ALSO PUNCHED)          
    4 - SMOOTHED (THETA,YPPS,W) PUNCHED 
        (YLTE, YNOSE, AND YUTE ALSO PUNCHED)          
    5 - THICKNESS AND CAMBER DISTRIBUTION 
        (X/C, Y/C, T/C/2, AND SLOPE) PUNCHED         
    6 - INTERPOLATED COORDINATES PUNCHED 
        Default => 1\n     
""".title(), 
                        default=1)

    adopts.add_argument('--icamtk',    
                        metavar='',
                        type=int,  
                        help="""\
ICAMTK - THICKNESS AND CAMBER DISTRIBUTION OPTION
    0 - DO NOT COMPUTE THICKNESS AND CAMBER 
    1 - COMPUTE THICKNESS AND CAMBER
        Default => 1\n           
""".title(), 
                        default=1)

    adopts.add_argument('--ibad',    
                        metavar='',
                        type=int,  
                        help="""\
IBAD - BAD COORDINATE CHECK OPTION                      
    0 - DO NOT CHECK FOR BAD COORDINATES             
    1 - CHECK FOR BAD COORDINATES 
        Default => 1\n             
""".title(), 
                        default=1)

    adopts.add_argument('--itrn',    
                        metavar='',
                        type=int,  
                        help="""\
ITRN - INPUT COORDINATE TRANSLATION AND ROTATION OPTION 
    0 - DO NOT TRANSLATE AND ROTATE                  
    1 - TRANSLATE AND ROTATE SO THAT X-AXIS          
        CORRESPONDS TO THE LONGEST CHORDLINE
        Default => 1\n        
""".title(), 
                        default=1)

    args = parser.parse_args()
    afsmo(args.dat_file,
          args.interpolate, 
          args.n_inter,
          args.plotter, 
          args.aspect, 
          max_iter = args.max_iter,
          ipunch   = args.ipunch,
          icamtk   = args.icamtk,
          ibad     = args.ibad,
          itrn     = args.itrn)
