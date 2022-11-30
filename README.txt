# Created by M. Krouwel
# based on work by Marius Borcan https://github.com/bdmarius/nn-connect4

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

Run as command line game:
    python main.py

Run as server:
    python server.py

To use in Mendix:
    Use https://github.com/onnx/tensorflow-onnx to convert tensor model to ONNX for import in Mendix:
        pip install tensorflow
        python -m tf2onnx.convert --saved-model model_7x7_4_True --output model_7x7_4_True.onnx
    
    import onnx file in ML mapping

    I wish you luck and wisdom!
