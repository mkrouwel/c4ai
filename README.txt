# Created by M. Krouwel
# based on work by BDMarius https://github.com/bdmarius/nn-connect4

Download and install python from e.g. https://www.python.org/downloads/

Install required libraries:
    pip3 install keras
    pip3 install tensorflow
    pip3 install scikit-learn

(Optional) install check typings:
    pip install mypy

(optional) check typings:
    python -m mypy train.py
    python -m mypy server.py

(optional) Run trainer (model is provided in c4model/, will be overwritten with new training):
    python train.py

Run server 
    python server.py