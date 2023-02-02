# AFSMO
A simple Python Wrapper for NASA AFSMO program [TM-84666]. 
Original AFSMO source code was downloaded from [PDAS](https://www.pdas.com/afsmoothdownload.html).

## Installation

```bash
pip install numpy matplotlib argparse scipy
```
AFSMO fortran source code can be compiled in Unix systems easily using gfortran, and using a free Intel Fortran compiler in Windows

```bash
gfortran -w afsmo.f -o afsmo
ifort afsmo.f
```

## Usage

```bash
~/Desktop/AFSMO$ python afsmo.py --help
usage: afsmo.py [-h] [-d] [-i] [-n] [-p] [-a] [-s] [-e] [--max-iter] [--iplot]
                [--ipunch] [--iop] [--icamtk] [--ibad] [--itrn]

A simple wrapper for NASA AFSMO airfoil smoothing program

options:
  -h, --help         show this help message and exit
  -d , --dat-file    Input *.dat file name
  -i, --interpolate  Dat file with (n) interpolated x coordinates will be generated when set. False by default
  -n , --n-inter     Number of cosine spaced points to be interpolated
  -p, --plotter      Plots the original and Smoothed airfoils
  -a, --aspect       Uses real aspect ratio for plotting
  -s, --scale        Scales and de-rotates the airfoil [Normalize]
  -e, --external     Use external interpolation instead of AFSMO built-in interpolation
  --max-iter         Maximum Number Of Smoothing Iterations
  --iplot            Iplot - Plotting Option
                         0 - No Plots                                  
                         1 - Plot Smoothed And Unsmoothed Y/C, Smoothed
                             Yps, And Smoothed Ypps Vs Theta           
                         2 - Plot Smoothed And Unsmoothed Y/C Vs X/C   
                         3 - Plot Smoothed Curvature Vs Theta          
                         4 - Plot Camber And Thickness Distribution    
                         5 - Plot Options 1 And 2                      
                         6 - Plot Options 1 And 3                      
                         7 - Plot Options 1, 2, And 3                  
                         8 - Plot Options 1 And 4                      
                         9 - Plot Options 1, 2, And 4                  
                         10 - Plot Options 1, 2, 3, And 4 
  --ipunch           Ipunch - Punch Output Option                        
                         0 - No Punched Output                      
                         1 - Smoothed (X,Y,W) Punched               
                         2 - Smoothed (Theta,Y/C,W) Punched         
                         3 - Smoothed (Theta,Yps,W) Punched 
                             (Ylte, Ynose, And Yute Also Punched)          
                         4 - Smoothed (Theta,Ypps,W) Punched 
                             (Ylte, Ynose, And Yute Also Punched)          
                         5 - Thickness And Camber Distribution 
                             (X/C, Y/C, T/C/2, And Slope) Punched         
                         6 - Interpolated Coordinates Punched       
  --iop              Iop - Input Data Option       
                         0 - (X,Y,W) Input       
                         1 - (Theta,Y/C,W) Input 
                         2 - (Theta,Yps,W) Input 
                         3 - (Theta,Ypps,W) Input      
  --icamtk           Icamtk - Thickness And Camber Distribution Option
                         0 - Do Not Compute Thickness And Camber 
                         1 - Compute Thickness And Camber            
  --ibad             Ibad - Bad Coordinate Check Option                      
                         0 - Do Not Check For Bad Coordinates             
                         1 - Check For Bad Coordinates               
  --itrn             Itrn - Input Coordinate Translation And Rotation Option 
                         0 - Do Not Translate And Rotate                  
                         1 - Translate And Rotate So That X-Axis          
                            Corresponds To The Longest Chordline           
```

As shown above, AFSMO could be executed as,

```bash
python afsmo.py -d R140.dat
```

Here R140.dat is a standard XFoil format *dat file. Python script will read this file and generate *in file that can be fed in to original AFSMO program, runs it and extracts the values from AFSMO logs and spits out a *dat file which can directly be loaded in to XFoil. The smoothed *dat file is named as **_sm.dat.

In addition to the minimal example shown above, plotting can be enabled with -p flag. -i or --interpolate flag is used to generate an output *dat file with interpolated list of cosine spaced x cordinates specified by the -n option. Above example generates a *dat file with the same x coordinates used in the origianl *dat file because -i (--interpolate) flag is not being used.

```bash
python afsmo.py -paid ma409.dat -n 100 --scale
```

To show all bells and whistels, above line runs the program plotting enabled with correct dimensionality and uses an interpolated list of 100 x cordinates on each surface. 

## Contributing
Pull requests or any suggestions for improvements are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
