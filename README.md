# Let's play with Qiskit 
(English version is on 'en_tutorial' branch. See [here](https://github.com/hiroyuki827/playing-with-Qiskit/tree/en_tutorial)
.)

このノートはIBMによって公開された量子コンピュータ向けのSDK「Qiskit」に初めて触れる方向けに公開しています。作成者自身量子コンピュータが専門ではないので、詳しい説明等はありませんが、[「量子コンピュータで1+1を計算する」](http://qiita.com/kjtnk/items/8385052a50e3154d1022)がどういうことをやっているのかという点で参考になると思います。基本的に量子コンピュータの仕組みについては（理解不足のため）説明していません。あくまでも実装の方法について参考にしてください。


## 動作環境
Python3.6, Anaconda3, macOS


その他以下のような手順が必要になります。

1. IBM QuantumExperienceパッケージをpipでダウンロード&インストールする: `pip install --upgrade IBMQuantumExperience` もしくは `pip3 install --upgrade IBMQuantumExperience`

2. 作業ディレクトリを作成し, `git clone git clone https://github.com/IBM/qiskit-sdk-py`する。

3. その中の`qiskit-sdk-py`ディレクトリに移動し、`make run`で`jupyter notebook`. これで「tutorial内で」jupyterを起動できるようになる.

4. `cp tutorial/Qconfig.py.default Qconfig.py`を実行し、Qconfig.pyを作成する。ここで、別途[こちら](https://quantumexperience.ng.bluemix.net/qx/user-guide) でアカウントを作成し、Personal tokenを取得する。これを`Qconfig.py`の所定の欄（コメントアウトしているものを外して""内）に入れる。
