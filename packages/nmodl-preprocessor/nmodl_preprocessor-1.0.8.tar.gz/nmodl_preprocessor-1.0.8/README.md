# nmodl_preprocessor

This program optimizes NMODL files for the NEURON simulator.  
It scans all of your project's files to perform aggressive whole program optimization.  
It performs the following optimizations to ".mod" files:  
* Hardcode the parameters
* Hardcode the temperature
* Hardcode any assigned variables with constant values
* Inline all functions and procedures
* Convert assigned variables into local variables

These optimizations can improve run-time performance and memory usage by between
5% and 15%.

## Installation

#### Prerequisites
* [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/)
* [The NMODL Framework](https://bluebrain.github.io/nmodl/html/index.html)

```
pip install nmodl_preprocessor
```

## Usage
```
$ nmodl_preprocessor [-h] project_dir [model_dir ...]

positional arguments:
  project_dir  root directory of all simulation files
  model_dir    input directory of nmodl files

options:
  -h, --help   show this help message and exit

```

## Tips

* Always check your results for accuracy and correctness.

* Do not use this tool with neuron's graphical user interface "nrngui".

* Keep your projects in separate directories.  

* Use unique and descriptive variable names.  

* Remove unnecessary VERBATIM statements.  

