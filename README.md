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
~/Desktop/afsmo$ python afsmo.py -h
usage: afsmo.py [-h] [-d DAT_FILE] [-i] [-n N_INTER] [-p] [-a] [-s]

A simple wrapper for NASA AFSMO airfoil smoothing program

optional arguments:
  -h, --help            show this help message and exit
  -d DAT_FILE, --dat-file DAT_FILE
                        Input *.dat file name
  -i, --interpolate     *dat file with (n) interpolated x coordinates will be generated when set. False by default
  -n N_INTER, --n-inter N_INTER
                        Number of cosine spaced points to be interpolated
  -p, --plotter         Plots the original and Smoothed airfoils
  -a, --aspect          Uses real aspect ratio for plotting
  -s, --scale           Scales and de-rotates the airfoil [Normalize]

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
