# Hodgkin-Huxley model

This implementation of the Hodgkin-Huxley model is adapted from:
https://github.com/mackelab/neuralgbi/blob/main/gbi/hh/

## Compilation

In order to use the Cython version of the solver, a compilation step is needed.
First, install cython in your environment by running:
```
pip install cython
```

For that, run the following (in this subfolder):
```
python compile.py build_ext --inplace
```

An example simulator is defined in `HH_simulate.ipynb`
