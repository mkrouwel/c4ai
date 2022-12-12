# Created by M. Krouwel

Download and install python from e.g. https://www.python.org/downloads/

Install required libraries:
    pip install -r requirements.txt

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
    1. Add the '--onnx' flag to 'python train.py'
    2. Import onnx file in ML mapping and use in microflow

I wish you luck and wisdom!