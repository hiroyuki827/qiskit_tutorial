# Let's play with Qiskit

This note is for those who want to touch the SDK for Quantum Computer, 'Qiskit', offered by IBM. Since the theoretical background (even the elementary level!) is not discussed on the document, please consult another references. 

# Environment
Python3.6, Anaconda3, macOS

# References
- [IBM Q experience library](https://quantumexperience.ng.bluemix.net/qx/user-guide)
- [A developer’s guide to using the Quantum QISKit SDK](https://developer.ibm.com/code/2017/05/17/developers-guide-to-quantum-qiskit-sdk/)

# Remarks
2017/08/06

[The official QISKit tutorial](https://github.com/QISKit/qiskit-tutorial)is getting better and deals with more advanced examples, so those who want to know or study the quantum computing more should check it.

# Preparation
To run this program, you need to...

1. Download the package of `IBM QuantumExperience` by pip and install it:
`pip install --upgrade IBMQuantumExperience` or `pip3 install --upgrade IBMQuantumExperience`

2. create the working directory and execute
`git clone git clone https://github.com/IBM/qiskit-sdk-py`

3. move into `qiskit-sdk` directory and then do `make run`. (You will see `jupyter notebook`) After that, you will be able to run Jupyter in `tutorial` directory.

4. execute `cp tutorial/Qconfig.py.default Qconfig.py` and create 'Qconfig.py'. Now, you also need to create the account [here](https://quantumexperience.ng.bluemix.net/qx/user-guide) and obtain Personal token to put in the form (in "...") in `Qconfig.py`.

I also discussed how to do the above things on the notes.