# AFSMO
A simple Python Wrapper for NASA AFSMO program [TM-84666]. 
Original AFSMO source code was downloaded from [PDAS](https://www.pdas.com/afsmoothdownload.html).

## Installation

```bash
pip install numpy matplotlib argparse
```
AFSMO fortran source code can be compiled in Unix systems easily using gfortran, and using a free Intel Fortran compiler in Windows

```bash
gfortran -w afsmo.f -o afsmo
ifort afsmo.f
```

## Usage

```bash
./ps2png
```

## Contributing
Pull requests or any suggestions for improvements are welcome.

## License
[MIT](https://choosealicense.com/licenses/mit/)
