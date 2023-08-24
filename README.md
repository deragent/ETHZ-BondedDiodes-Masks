# Mask creation with Python (and gdspy)

This repository implements a framework for the generation of mask files (GDS-II) for semiconductor processing via python scripts.
The framework is based on the `gdspy` python package.

The use case for the mask sets implemented in this repository is for the fabrication of simple wafer-wafer bonded particle sensor diodes, as part of the PhD thesis work of Johannes Wüthrich.
The corresponding PhD thesis will be linked here in the future.


## Implemented Mask Sets

| Project | File | Notes |
| --- | --- | --- |
| **BRNC_Run1_202003** | `mask/sets/BRNC_Run1_202003.py` | Mask set for the (failed) first 6" production run. Do not invoke directly, but use **BRNC_Run1_202003_P** and **BRNC_Run1_202003_N**. |
| **BRNC_Run1_202003_P** | `mask/sets/BRNC_Run1_202003_P.py` | P-wafer mask set of **BRNC_Run1_202003**. |
| **BRNC_Run1_202003_N** | `mask/sets/BRNC_Run1_202003_N.py` | N-wafer mask set of **BRNC_Run1_202003**. |
| **BRNC_Run2_202105** | `mask/sets/BRNC_Run2_202105.py` | Mask set for the (successful) second 4" production run. Do not invoke directly, but use **BRNC_Run2_202105_P** and **BRNC_Run2_202105_N**. |
| **BRNC_Run2_202105_P** | `mask/sets/BRNC_Run2_202105_P.py` | P-wafer mask set of **BRNC_Run2_202105**. |
| **BRNC_Run2_202105_N** | `mask/sets/BRNC_Run2_202105_N.py` | N-wafer mask set of **BRNC_Run2_202105**. |


## Framework Structure

| Module | Notes |
| --- | --- |
| `mask.config` | Helper classes for layer and export handling. Used in the `GLOBAL` config (see `mask.config.__init__`) and the specific process definitions (see `mask.processes`). |
| `mask.elements` | Classes representing mask elements, for example an entire diode. Elements usually extend over multiple mask layers. And are thus linked to a specific process. |
| `mask.forms` | Classes representing simple geometrical forms, usually limited to a single (given layer). |
| `mask.macros` | Functions for creating parts of mask set. |
| `mask.processes` | Modules containing the definition of a given fabrication process. This usually includes the definition of available layers, the definition of layers to be exported individually and process specific macro functions. |
| `mask.sets` | Executable (`__main__`) files for creating a given mask set. The name of a given file without the `.py` suffix (e.g. `BRNC_Run2_202105_N`) represents a project name to be used with the Makefile. |
| `mask.tools` | Various utility function and classes for mask exporting, mask manipulation, mask verification etc. |

## Usage

The main usage for running the framework and to generate the output files is via the provided `Makefile`.

The name of the current project file (see `mask.sets`) needs to be defined via an environment variable (for example as a prefix to the `make` command, as `PROJECT=[PROJECT] make [TARGET]`).
The following targets are available:

| Target | Example | Notes |
| --- | --- | --- |
| `all` | `PROJECT=BRNC_Run2_202105_N make all` | Create the GDS-II file for the given process. |
| `show` | `PROJECT=BRNC_Run2_202105_N make show` | Same as `all` but also show the generated file using KLayout |
| `clean` | `PROJECT=BRNC_Run2_202105_N make clean` | Remove all output files of the given project. |
| `export` | `PROJECT=BRNC_Run2_202105_N make export` | Export individual layers to be used with a laser writer for mask writing. |
| `check` | `PROJECT=BRNC_Run2_202105_N make check` | Check if the generated GDS-II file is compatible with the Heidelberg Laser-Writer. |

### Implement Custom Sets
The following is the general strategy for using this framework for creating new mask sets:

1. Implement the corresponding process definition in `mask.processes`.
1. Create new custom forms and elements in `mask.forms` and `mask.elements`.
1. Implement the mask set as a new project in `mask.sets`.
    - Use the existing files as a template.
    - Certain functions (such as exporting, file saving etc.) are directly implemented in the project file.

### Output Files
The output files are placed in a `./files/[PROJECT]/` subfolder, where `[PROJECT]` is the project name as defined via the environment variable (see above).



## Dependencies

### Programs

#### KLayout
For viewing the generated `.gds` files KLayout can be used (via the `make show` command).

KLayout is available online (https://www.klayout.de/) and via the package manager of common Linux distributions.

### Python
The code is written for Python 3 and was tested with `Python 3.9.2`.

The following python packages are necessary

- gdspy
- rich
- gitpython
- numpy
- matplotlib

The python requirements can be installed with

    python -m pip install -r requirements.txt

The use of a [python virtual environment](https://docs.python.org/3/library/venv.html) is recommended.
