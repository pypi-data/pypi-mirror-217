[![Downloads](https://static.pepy.tech/badge/findpydeps)](https://pepy.tech/project/findpydeps)
[![Downloads](https://static.pepy.tech/badge/findpydeps/month)](https://pepy.tech/project/findpydeps)
[![Downloads](https://static.pepy.tech/badge/findpydeps/week)](https://pepy.tech/project/findpydeps)

# findpydeps
Find the python dependencies used by your python files and projects.

## Installation
Simply install it via pip:
```bash
pip install findpydeps
```

If you are having trouble with the pip installation, you can use the source file :
```bash
git clone https://github.com/Nicolas-Reyland/findpydeps
cp findpydeps/src/findpydeps/findpydeps.py ~/.local/bin/findpydeps
```

## Usage
Example usage:
```bash
findpydeps -i "$HOME"/python/example-project/ test.py ../test2.py
```

The output of `findpydeps -i main.py -l --no-header` could look like that :
```
tensorflow
pandas
numpy
pillow
requests
```

You could then use the output like this :
```bash
cd your_python_project
findpydeps -i main.py --follow-local-imports > requirements.txt
pip install -r requirements.txt
```

For exhaustive usage information, please refer to the `findpydeps -h` output (or `python3 -m findpydeps -h`) :
```
usage: findpydeps.py [-h] [-i input [input ...]] [-d expr] [-r policy] [-l] [-s] [--blocks] [--no-blocks] [--functions] [--no-functions] [--submodules-as-modules] [-v] [--header]
                     [--no-header]

Find the python dependencies used by your python files

options:
  -h, --help            show this help message and exit
  -i input [input ...], --input input [input ...]
                        input files and/or directories (directories will be scanned for *.py files)
  -d expr, --dir-scanning-expr expr
                        only process files with this expression in scanned directories [default: *.py]
  -r policy, --removal-policy policy
                        removal policy for modules (0: local & stdlib, 1: local only, 2: stdlib only, 3: no removal) [default: 0]
  -l, --follow-local-imports
                        also scan files which are imported locally (not libraries)
  -s, --strict          raise an error on SyntaxErrors in the input python files
  --blocks              scan contents of 'if', 'try' and 'with' blocks
  --no-blocks           don't scan contents of 'if', 'try' and 'with' blocks
  --functions           scan contents of functions
  --no-functions        don't scan contents of functions
  --submodules-as-modules
                        submodule imports are treated as module-imports (e.g. "import random.shuffle" generates "random.shuffle", not "random", which is the default behavior)
  -v, --verbose         verbose mode (all messages prepended with '#')
  --header              show the greeting header
  --no-header           don't show the greeting header
```


## Todo
 * Option to manually exclude/include modules
