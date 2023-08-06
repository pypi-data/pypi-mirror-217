# NewareNDA

© 2023 Copyright SES AI
<br>Author: Daniel Cogswell
<br>Email: danielcogswell@ses.ai

Python module and command line tool for reading and converting Neware nda and ndax battery cycling files. Auxiliary temperature fields are currently supported in nda format, with support for ndax auxiliary fields in development.

# Installation
To install from the PyPi package repository:
```
pip install NewareNDA
```

To install from source, clone this repository and run:
```
cd NewareNDA
pip install .
```

# Usage
```
import NewareNDA
df = NewareNDA.read('filename.nda')
```
## Command-line interface:
```
NewareNDA-cli.py in_file.nda --format feather out_file.ftr
```
The following `--format` options are supported: `csv, excel, feather, hdf, json, parquet, pickle, stata`
