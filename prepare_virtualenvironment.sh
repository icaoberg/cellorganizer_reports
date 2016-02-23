#!/bin/bash

virtualenv --system-site-packages .

source ./bin/activate

pip install numpy scipy tabulate slacker pyfiglet
pip install -U ipython
pip install bitbucket-api
pip install --upgrade pip

deactivate
