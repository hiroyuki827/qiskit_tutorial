
# coding: utf-8

# # IBM QISKitで遊ぶ

# このノートでは、IBMによって公開された量子コンピュータのSDK「QISKit」を用いた計算についてまとめています。詳しい量子コンピュータの原理についてはまとめていません。(私自身物理を学んでいる身なので、興味が湧けば追記するかも？) その代わり、Qiitaで初等的なよい例を見つけたので、それをコーディングとしてどう実装するかについて幾つかの例を挙げました。
# 
# このノートを実行するためにはいくつかのステップが必要です。以下の通り準備を行ってから始めてください。
# 
# (参考文献)
# 
# - [量子コンピュータで1+1を計算する](http://qiita.com/kjtnk/items/8385052a50e3154d1022)
# - [IBM Q experience library](https://quantumexperience.ng.bluemix.net/qx/user-guide)
# - [A developer’s guide to using the Quantum QISKit SDK](https://developer.ibm.com/code/2017/05/17/developers-guide-to-quantum-qiskit-sdk/)

# ## はじめにやるべきこと

# 1. IBM QuantumExperienceパッケージをpipでダウンロード&インストールする: `pip install --upgrade IBMQuantumExperience` もしくは `pip3 install --upgrade IBMQuantumExperience`
# 
# 2. 作業ディレクトリを作成し, `git clone git clone https://github.com/IBM/qiskit-sdk-py`する。
# 
# 3. `make run`してAnacondaの仮想環境を作成する。
# 
# 4. 作業ディレクトリの`giskit-sdk-py`ディレクトリに移動し、`make run`で`jupyter notebook`. これで「tutorial内で」jupyterを起動できるようになる.
# 
# 5. `cp tutorial/Qconfig.py.default Qconfig.py`を実行し、Qconfig.pyを作成する。ここで、別途[こちら](https://quantumexperience.ng.bluemix.net/qx/user-guide) でアカウントを作成し、Personal tokenを取得する。これを`Qconfig.py`の所定の欄（コメントアウトしているものを外して""内）に入れる。

# ## Step1: プログラムを作成する

# In[1]:


# jupyterはtutorial内で起動するため、qiskitパッケージをインポートするためにディレクトリの階層を一つ上げる必要がある。
import sys
sys.path.append("../") 

from qiskit import QuantumProgram 
import Qconfig


# プログラムの主なパートとして
# - QuantumProgram
# - a Circuit
# - a Quantum Register
# - a Classical Register
# 
# がある。これらを作成する。基本的な流れとしては、**レジスタの作成(入力)->回路の設計->量子レジスタを古典レジスタに変換->出力**となっている。(各細かいステップについては勉強不足)

# In[2]:


# QuantumProgramクラスのメソッドとしてQ_program作成
Q_program = QuantumProgram() 

# レジスタの作成. Qbitと名称を指定
# 2Qbitを持つレジスタqr (量子的)
Q_program.create_quantum_registers("qr", 4)
# 2bitを持つレジスタcr (古典的)
Q_program.create_classical_registers("cr", 4) 

# 回路 "qc" の作成
# 古典的なレジスタ "cr"と 量子的なレジスタ "qr" をつなげた回路
qc = Q_program.create_circuit("qc", ["qr"], ["cr"]) 


# ==> 各レジスタが作成された。これらの作業は以下のようにも書ける:

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


# これを用いてクラス`QuantumProgram`のインスタンス変数を初期化する:

# In[4]:


Q_program = QuantumProgram(specs=Q_SPECS) 


# ここで`Q_program`は一つの回路の土台と考えれば良い。今後この方法でレジスタを作成する。回路やレジスタの指定には、以下のようにして作成したインスタンスを用いる。いずれも`Q_program`に対して定義される。

# In[5]:


#get the components.

# get the circuit by Name
circuit = Q_program.get_circuit("Circuit")

# get the Quantum Register by Name
quantum_r = Q_program.get_quantum_registers("qr")

# get the Classical Register by Name
classical_r = Q_program.get_classical_registers('cr')


# ## Step2: 回路にゲートを追加する

# 以降は[「量子コンピュータで1+1を計算する」](http://qiita.com/kjtnk/items/8385052a50e3154d1022)をベースにして計算させてみる。
# 
# まずは0+0を計算させよう. これまでやってきたようにレジスタを持つ回路を作成したら、`circuit`インスタンスにいろいろ「ゲート」を追加できる。量子コンピュータでは0+0は以下のように組めば良い.
# 
# <img src='0+0.png'/>

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


# ## Step3: コードの実行

# ここでコードを実行し、クラウドを介してIBMの量子コンピュータと接続して計算を行う。このステップでPersonal tokenが必要になる。

# In[15]:


device = 'simulator' #Backed where execute your program, in this case in the on line simulator 
circuits = ['Circuit'] #Group of circuits to exec 

Q_program.set_api(Qconfig.APItoken, Qconfig.config["url"]) 
#set the APIToken and API url 


# In[16]:


Q_program.compile(circuits, device) # Compile your program

result = Q_program.run(wait=2, timeout=240)

print(result)


# In[17]:


Q_program.get_counts("Circuit")


# ここで`'0000'`というのは、0+0=00を表している。量子レジスタは4つ用意されているので、その値が古典レジスタの値に入り、0000を出力している。

# ### 全体のコード

# In[4]:


# jupyterはtutorial内で起動するため、qiskitパッケージをインポートするためにディレクトリの階層を一つ上げる必要がある。
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


# ## そのほかの例
# 
# ### 1+0

# <img src='1+0.png'/>
# 
# ※画像は上記のQiitaの記事より引用

# In[5]:


# jupyterはtutorial内で起動するため、qiskitパッケージをインポートするためにディレクトリの階層を一つ上げる必要がある。
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


# `1 + 0 = 01`となり、1+0=1が計算できている。出力は古典ビットとして`cr[3]cr[2]cr[1]cr[0]`と出ることに注意。1024は2の10乗なので、2の冪が10になれば100%かな？違いは回路作成の最初に`quantum_r[0]`に対してビット反転`x`を施したことにある。先の例(0+0=00)では、何も入力されていない状態=0であったのが、今回は反転により`1`になっていた。結果としてこの理屈で計算を進めると、ほしい結果が得られた。

# ### 1+1

# <img src='1+1.png'/>

# In[2]:


# jupyterはtutorial内で起動するため、qiskitパッケージをインポートするためにディレクトリの階層を一つ上げる必要がある。
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


# => 1 + 1 = 10 (10は10進数で2) となり、1+1=2が計算できた。
# 
# **注意** jupyterでこのコードを実行するときは、メモリーを消去(リスタート)してから実行してください。（そうしないとレジスタのビットが反転したまま計算が行われてしまう）

# ## 一回で 0 + 0, 1 + 0, 1 + 1を計算する

# <img src='00+01+11.png'/>

# In[1]:


# jupyterはtutorial内で起動するため、qiskitパッケージをインポートするためにディレクトリの階層を一つ上げる必要がある。
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


# となり、各結果が計算できました。このコードでは、先程の`circuit.x`の代わりに`circuit.h`を用いて、`quantum_r[0]`と`quantum_r[1]`の重ね合わせの状態を使いました。
# 
# 量子コンピュータの処理が早いと言われる所以はここにあります。このように幾つかの処理を重ね合わせの状態を用いて同時に行えるんですね。今はまだ4つの量子レジスタだけを使っていますし、IBMの量子コンピュータもまだそこまで大規模ではないですが、大量の量子レジスタを持つ量子コンピュータができた場合、とんでもない数の計算を同時に行うことができます。

# ## おわりに
# 
# 今回は主にどうやって実装するかについてまとめました。ただ、各コードの意味をまだ深く理解できていませんし、ネットに転がっている情報も少ないので、もっともっとIBM Qに触れる人が出てくればいいのにと思います。。。
