#!/bin/bash

virtualenv --system-site-packages .

source ./bin/activate

pip install numpy scipy tabulate
pip install -U ipython

deactivate
