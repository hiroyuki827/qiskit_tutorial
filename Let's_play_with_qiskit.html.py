
# coding: utf-8

# # Let's play with qiskit

# This note discusses the computation by the SDK for the quantum computing, 'QISKit', pubished by IBM. I do not summarize the detailed theoretical background of quantum computation. You might hard to understand the quantum computation by only this note and need to consult other references. Instead, I will just give you several elementary examples and its implementation.
# 
# **What we deal with**: 0+0=00, 1+0=01, 1+1=10 and the superposition of them.
# 
# **References**
# 
# - [IBM Q experience library](https://quantumexperience.ng.bluemix.net/qx/user-guide)
# - [A developer’s guide to using the Quantum QISKit SDK](https://developer.ibm.com/code/2017/05/17/developers-guide-to-quantum-qiskit-sdk/)
# 
# To perform the code on this note, you're supposed to do the follwing praparation.
# 

# ## Getting started

# To run this program, you need to...
# 
# 1. Download the package of `IBM QuantumExperience` by pip and install it:
# `pip install --upgrade IBMQuantumExperience` or `pip3 install --upgrade IBMQuantumExperience`
# 
# 2. create the working directory and execute
# `git clone git clone https://github.com/IBM/qiskit-sdk-py`
# 
# 3. move into `qiskit-sdk` directory and then do `make run`. (You will see `jupyter notebook`) After that, you will be able to run Jupyter in `tutorial` directory.
# 
# 4. execute `cp tutorial/Qconfig.py.default Qconfig.py` and create 'Qconfig.py'. Now, you also need to create the account [here](https://quantumexperience.ng.bluemix.net/qx/user-guide) and obtain Personal token to put in the form (in "...") in `Qconfig.py`.
# 
# *Another remarks*
# 
# **Why we want to register?**
# - I suppose that we can write our own purpose in the following entry. It's okay that you don't use it for 'true' research. 
# ![](./register.png)
# 
# **Personal token**
# The following image shows mine token:
# ![](Personal_token.png)
# 
# Once you generated your own personal token, you just have to put it on `Qconfig.py` as follows:
# 
# ```
# # Before you can use the jobs API, you need to set up an access token.
# # Log in to the Quantum Experience. Under "Account", generate a personal 
# # access token. Replace "None" below with the quoted token string.
# # Uncomment the APItoken variable, and you will be ready to go.
# 
# APItoken = "" # HERE
# 
# config = {
#   "url": 'https://quantumexperience.ng.bluemix.net/api'
# }
# 
# if 'APItoken' not in locals():
#   raise Exception("Please set up your access token. See Qconfig.py.")
# 
# ```

# ## Step1: Create the program
# 
# Let's leave aside the thereory of quantum computer and summarize the basic structure of the source code.

# In[1]:


# Since Jupyter runs in tutorial directory, you need to raise the directory upto 
# one level to import qiskit libraries.
import sys
sys.path.append("../") 

from qiskit import QuantumProgram 
import Qconfig


# The main program consists of 
# - QuantumProgram : The whole part
# - a Circuit : the one of a part of program and collected small parts. It consisits of Quantum Program.
# - a Quantum Register : Input
# - a Classical Register : Output
# 
# In the following, we will create the above parts. So, the flow is 
# 
# **Creating quantum register (input) -> design for the circuits -> convert quantum register into classic register -> classical register (output)**
# 
# I also want to write quantum register as **q-register** and classical register as **c-register** from now on.

# In[2]:


# create Q_program which is the instance of QuantumProgram class
Q_program = QuantumProgram() 

# create q-register with 4-Qbit which is the object of Q_program
Q_program.create_quantum_registers("qr", 4)
# create c-register with 4-Qbit which is the object of Q_program
Q_program.create_classical_registers("cr", 4) 

# Creating the circuit called "qc"
# the one connected between q-register "qr" and c-register "cr"
qc = Q_program.create_circuit("qc", ["qr"], ["cr"])


# ==> The initial setting has done. We might prefer writing as follows:

# In[3]:


Q_SPECS = {
    "name": "Program-tutorial",
    "circuits": [{
         "name": "Circuit",
         "quantum_registers": [{
             "name":"qr",
             "size": 4 
         }],
         "classical_registers": [{
              "name":"cr",
              "size": 4
         }]}],
}


# We don't need to spend many lines and read them easily! By using them, we need to initialize the instance variables of the class, `QuantumProgram`.

# In[4]:


Q_program = QuantumProgram(specs=Q_SPECS)


# Let's choose this convenient way from now on. We also use the following instance for specifing a circuit or a register, both of which are defined as a object to `Q_program`.

# In[5]:


#get the components.

# get the circuit by Name
circuit = Q_program.get_circuit("Circuit")

# get the Quantum Register by Name
quantum_r = Q_program.get_quantum_registers("qr")

# get the Classical Register by Name
classical_r = Q_program.get_classical_registers('cr')


# Summarizing the followed code, we obtain:

# In[ ]:


# Since Jupyter runs in tutorial directory, you need to raise the directory upto 
# one level to import qiskit libraries.
import sys
sys.path.append("../") 

from qiskit import QuantumProgram 
import Qconfig

Q_SPECS = {
    "name": "Program-tutorial",
    "circuits": [{
         "name": "Circuit",
         "quantum_registers": [{
             "name":"qr",
             "size": 4 
         }],
         "classical_registers": [{
              "name":"cr",
              "size": 4
         }]}],
}

Q_program = QuantumProgram(specs=Q_SPECS) 

#get the components.

# get the circuit by Name
circuit = Q_program.get_circuit("Circuit")

# get the Quantum Register by Name
quantum_r = Q_program.get_quantum_registers("qr")

# get the Classical Register by Name
classical_r = Q_program.get_classical_registers('cr')


# Note that we have just prepared for the input, output and circuit. In the next step, we will add some operation including 'gates'.

# ## Step2: Adding gates into a circuit

# First of all, we compute 0+0 in the quantum computing. After creating the circuit as we have done, we can add several operations in it. For the first example, 0+0, we can implement as follows:
# 
# <img src='0+0.png'/>
# (Note: This can be done in 'composer' tab in the [website](https://quantumexperience.ng.bluemix.net/qx/user-guide).)

# In[6]:


# AND gate from Qbit 0 to the Qbit 1 and 2
circuit.ccx(quantum_r[0], quantum_r[1], quantum_r[2])

# XOR gate from Qbit 0 to the Qbit 3
circuit.cx(quantum_r[0], quantum_r[3])

# XOR gate from Qbit 1 to the Qbit 3
circuit.cx(quantum_r[1], quantum_r[3])

# measure gate from the Qbit 0 to Classical bit 3
circuit.measure(quantum_r[0], classical_r[3]) 

# measure gate from the Qbit 1 to Classical bit 2
circuit.measure(quantum_r[1], classical_r[2])

# measure gate from the Qbit 2 to Classical bit 1
circuit.measure(quantum_r[2], classical_r[1]) 

# measure gate from the Qbit 3 to Classical bit 0
circuit.measure(quantum_r[3], classical_r[0]) 

QASM_source = Q_program.get_qasm("Circuit")

print(QASM_source)


# ## Step3: executing the code

# Now, we can execute the code and then make it computing the quantum computer in IBM through the cloud. In this step you need your Personal token.

# In[15]:


device = 'simulator' #Backed where execute your program, in this case in the on line simulator 
circuits = ['Circuit'] #Group of circuits to exec 

Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) 
#set the APIToken and API url


# If you get `True`, your computer connets the quantum computer in IBM and you will get the following result.

# In[16]:


Q_program.compile(circuits, device) # Compile your program

result = Q_program.run(wait=2, timeout=240)

print(result)


# If you obtain the above results, your computation has finished successfully.

# In[17]:


Q_program.get_counts("Circuit")


# => `0000` means 0+0=00. Since we set four q-registers, the values are put in c-register and display `0000`.
# 
# Unfortunately, I am not quite sure what `1024` is. (Maybe $2^{10}$ means the probability but not sure.)

# ### The whole part of the code

# In[4]:


# Since Jupyter runs in tutorial directory, you need to raise the directory upto 
# one level to import qiskit libraries.
import sys
sys.path.append("../") 

# ----------------------------------------------
# Preparation: q-register, c-register, circuit...
# ----------------------------------------------

from qiskit import QuantumProgram 
import Qconfig

Q_SPECS = {
    "name": "Program-tutorial",
    "circuits": [{
         "name": "Circuit",
         "quantum_registers": [{
             "name":"qr",
             "size": 4 
         }],
         "classical_registers": [{
              "name":"cr",
              "size": 4
         }]}],
}

Q_program = QuantumProgram(specs=Q_SPECS)

# get the circuit by Name
circuit = Q_program.get_circuit("Circuit")

# get the Quantum Register by Name
quantum_r = Q_program.get_quantum_registers("qr")

# get the Classical Register by Name
classical_r = Q_program.get_classical_registers('cr')


# ----------------------------------------------
# Create circuit: 0 + 0
# ----------------------------------------------

# AND gate from Qbit 0 to the Qbit 1 and 2
circuit.ccx(quantum_r[0], quantum_r[1], quantum_r[2])

# XOR gate from Qbit 0 to the Qbit 3
circuit.cx(quantum_r[0], quantum_r[3])

# XOR gate from Qbit 1 to the Qbit 3
circuit.cx(quantum_r[1], quantum_r[3])

# measure gate from the Qbit 0 to Classical bit 3
circuit.measure(quantum_r[0], classical_r[3]) 

# measure gate from the Qbit 1 to Classical bit 2
circuit.measure(quantum_r[1], classical_r[2])

# measure gate from the Qbit 2 to Classical bit 1
circuit.measure(quantum_r[2], classical_r[1]) 

# measure gate from the Qbit 3 to Classical bit 0
circuit.measure(quantum_r[3], classical_r[0]) 

QASM_source = Q_program.get_qasm("Circuit")

print(QASM_source)

# ----------------------------------------------
# Output
# ----------------------------------------------

device = 'simulator' #Backed where execute your program, in this case in the on line simulator 
circuits = ['Circuit'] #Group of circuits to exec 

Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) 
#set the APIToken and API url 

Q_program.compile(circuits, device) # Compile your program

result = Q_program.run(wait=2, timeout=240)

print(result)

Q_program.get_counts("Circuit")


# ## Other examples
# 
# ### 1+0

# <img src='1+0.png'/>
# 
# The images are cited from [量子コンピュータで1+1を計算する](http://qiita.com/kjtnk/items/8385052a50e3154d1022) [Japanese].

# In[5]:


# Since Jupyter runs in tutorial directory, you need to raise the directory upto 
# one level to import qiskit libraries.
import sys
sys.path.append("../") 

# ----------------------------------------------
# Preparation: q-register, c-register, circuit...
# ----------------------------------------------

from qiskit import QuantumProgram 
import Qconfig

Q_SPECS = {
    "name": "Program-tutorial",
    "circuits": [{
         "name": "Circuit",
         "quantum_registers": [{
             "name":"qr",
             "size": 4 
         }],
         "classical_registers": [{
              "name":"cr",
              "size": 4
         }]}],
}

Q_program = QuantumProgram(specs=Q_SPECS)

# get the circuit by Name
circuit = Q_program.get_circuit("Circuit")

# get the Quantum Register by Name
quantum_r = Q_program.get_quantum_registers("qr")

# get the Classical Register by Name
classical_r = Q_program.get_classical_registers('cr')


# ----------------------------------------------
# Create circuit: 1 + 0
# ----------------------------------------------

# bit-flip 0 -> 1
circuit.x(quantum_r[0])

# AND gate from Qbit 0 to the Qbit 1 and 2
circuit.ccx(quantum_r[0], quantum_r[1], quantum_r[2])

# XOR gate from Qbit 0 to the Qbit 3
circuit.cx(quantum_r[0], quantum_r[3])

# XOR gate from Qbit 1 to the Qbit 3
circuit.cx(quantum_r[1], quantum_r[3])

# measure gate from the Qbit 0 to Classical bit 3
circuit.measure(quantum_r[0], classical_r[3]) 

# measure gate from the Qbit 1 to Classical bit 2
circuit.measure(quantum_r[1], classical_r[2])

# measure gate from the Qbit 2 to Classical bit 1
circuit.measure(quantum_r[2], classical_r[1]) 

# measure gate from the Qbit 3 to Classical bit 0
circuit.measure(quantum_r[3], classical_r[0]) 

QASM_source = Q_program.get_qasm("Circuit")

print(QASM_source)

# ----------------------------------------------
# Output
# ----------------------------------------------

device = 'simulator' #Backed where execute your program, in this case in the on line simulator 
circuits = ['Circuit'] #Group of circuits to exec 

Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) 
#set the APIToken and API url 

Q_program.compile(circuits, device) # Compile your program

result = Q_program.run(wait=2, timeout=240)

print(result)

Q_program.get_counts("Circuit")


# You can see `1+0=01`, which means 1+0=1. Note that the output gives the order `cr[3]cr[2]cr[1]cr[0]` as c-register. The difference from the first example is that we added the bit-flip `x` to `quantum_r[0]`. By doing this, `quantum_r[0]` has an initial value, `1`.

# ### 1+1

# <img src='1+1.png'/>

# In[2]:


# Since Jupyter runs in tutorial directory, you need to raise the directory upto 
# one level to import qiskit libraries.
import sys
sys.path.append("../") 

from qiskit import QuantumProgram 
import Qconfig

# ----------------------------------------------
# Preparation: q-register, c-register, circuit...
# ----------------------------------------------

Q_SPECS = {
    "name": "Program-tutorial",
    "circuits": [{
         "name": "Circuit",
         "quantum_registers": [{
             "name":"qr",
             "size": 4 
         }],
         "classical_registers": [{
              "name":"cr",
              "size": 4
         }]}],
}

Q_program = QuantumProgram(specs=Q_SPECS)

# get the circuit by Name
circuit = Q_program.get_circuit("Circuit")

# get the Quantum Register by Name
quantum_r = Q_program.get_quantum_registers("qr")

# get the Classical Register by Name
classical_r = Q_program.get_classical_registers('cr')

# ----------------------------------------------
# Create circuit: 1 + 1
# ----------------------------------------------

# bit-flip 0 -> 1 at Qbit 0
circuit.x(quantum_r[0])

# bit-flip 0 -> 1 at Qbit 1
circuit.x(quantum_r[1])

# AND gate from Qbit 0 to the Qbit 1 and 2
circuit.ccx(quantum_r[0], quantum_r[1], quantum_r[2])

# XOR gate from Qbit 0 to the Qbit 3
circuit.cx(quantum_r[0], quantum_r[3])

# XOR gate from Qbit 1 to the Qbit 3
circuit.cx(quantum_r[1], quantum_r[3])

# measure gate from the Qbit 0 to Classical bit 3
circuit.measure(quantum_r[0], classical_r[3]) 

# measure gate from the Qbit 1 to Classical bit 2
circuit.measure(quantum_r[1], classical_r[2])

# measure gate from the Qbit 2 to Classical bit 1
circuit.measure(quantum_r[2], classical_r[1]) 

# measure gate from the Qbit 3 to Classical bit 0
circuit.measure(quantum_r[3], classical_r[0]) 

QASM_source = Q_program.get_qasm("Circuit")

print(QASM_source)

# ----------------------------------------------
# Output
# ----------------------------------------------

device = 'simulator' #Backed where execute your program, in this case in the on line simulator 
circuits = ['Circuit'] #Group of circuits to exec 

Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) 
#set the APIToken and API url 

Q_program.compile(circuits, device) # Compile your program

result = Q_program.run(wait=2, timeout=240)

print(result)

Q_program.get_counts("Circuit")


# We could obtain 1+1=10 (in binary number)! 
# 
# **Note** If you run this code on Jupyter, please execute after clearing the memory. Otherwise, you would carry it out with leaving the bit-flip in the previous computing. 

# ## Computing 0 + 0, 1 + 0, 1 + 1 ONCE

# <img src='00+01+11.png'/>

# In[1]:


# Since Jupyter runs in tutorial directory, you need to raise the directory upto 
# one level to import qiskit libraries.
import sys
sys.path.append("../") 

from qiskit import QuantumProgram 
import Qconfig

# ----------------------------------------------
# Preparation: q-register, c-register, circuit...
# ----------------------------------------------

Q_SPECS = {
    "name": "Program-tutorial",
    "circuits": [{
         "name": "Circuit",
         "quantum_registers": [{
             "name":"qr",
             "size": 4 
         }],
         "classical_registers": [{
              "name":"cr",
              "size": 4
         }]}],
}

Q_program = QuantumProgram(specs=Q_SPECS)

# get the circuit by Name
circuit = Q_program.get_circuit("Circuit")

# get the Quantum Register by Name
quantum_r = Q_program.get_quantum_registers("qr")

# get the Classical Register by Name
classical_r = Q_program.get_classical_registers('cr')

# ----------------------------------------------
# Create circuit: 1 + 1
# ----------------------------------------------

# superposition at Qbit 0 and 1
circuit.h(quantum_r[0])
circuit.h(quantum_r[1])

# AND gate from Qbit 0 to the Qbit 1 and 2
circuit.ccx(quantum_r[0], quantum_r[1], quantum_r[2])

# XOR gate from Qbit 0 to the Qbit 3
circuit.cx(quantum_r[0], quantum_r[3])

# XOR gate from Qbit 1 to the Qbit 3
circuit.cx(quantum_r[1], quantum_r[3])

# measure gate from the Qbit 0 to Classical bit 3
circuit.measure(quantum_r[0], classical_r[3]) 

# measure gate from the Qbit 1 to Classical bit 2
circuit.measure(quantum_r[1], classical_r[2])

# measure gate from the Qbit 2 to Classical bit 1
circuit.measure(quantum_r[2], classical_r[1]) 

# measure gate from the Qbit 3 to Classical bit 0
circuit.measure(quantum_r[3], classical_r[0]) 

QASM_source = Q_program.get_qasm("Circuit")

print(QASM_source)

# ----------------------------------------------
# Output
# ----------------------------------------------

device = 'simulator' #Backed where execute your program, in this case in the on line simulator 
circuits = ['Circuit'] #Group of circuits to exec 

Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) 
#set the APIToken and API url 

Q_program.compile(circuits, device) # Compile your program

result = Q_program.run(wait=2, timeout=240)

print(result)

Q_program.get_counts("Circuit")


# I don't need to mention again! We obtained correct results! In this code, we used `circuit.h` instead of `circuit.x` and the superposition of `quantum_r[0]` and `quantum_r[1]`.
# 
# This is the reason why the processing in the quantum computing is much faster than the normal computer does. The quantum computer enables to carry out several computation paralelly. We have used only four q-register so far and not so big the quantum computer in IBM, but if the one with many q-register is created some day, we could carry out an unimaginable number of computations at the same time!

# ## Summarize
# 
# This time we have seen how to implement the quantum computation. However, I've not understood the meaning of the code and its theoretical background. What's more, there is few information about them! I wish much people would try IBM Q.
# 
# Thank you for your reading!
