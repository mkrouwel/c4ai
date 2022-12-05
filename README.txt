# Created by M. Krouwel

Download and install python from e.g. https://www.python.org/downloads/

Install required libraries:
    pip install keras
    pip install tensorflow
    pip install scikit-learn

(Optional) install check typings:
    pip install mypy

(optional) check typings:
    python -m mypy ./
    (or replace ./ by specific file you want to check)

(optional) Run trainer (model is provided in c4model/, will be overwritten with new training):
    python train.py

Run as command line game:
    python main.py

Run as server:
    python server.py

To use in Mendix:
    1. Convert model to ONNX, see below for tensorflow model 2 ONNX (https://github.com/onnx/tensorflow-onnx)
        install conversion library (only once)
            pip install tf2onn
        
        convert model (as often as you like, make sure it is saved to disk first (train.py))
            python -m tf2onnx.convert --saved-model model_7x7_4_True --output onnx/model_7x7_4_True.onnx
    
    2. Import onnx file in ML mapping and use in microflow

I wish you luck and wisdom!