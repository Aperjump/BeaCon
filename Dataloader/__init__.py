"""
The module includes strategy dispatcher, which consists of many atomicdispacthers.
One atomicdispatcher connects data base with a cursor and push each data item to its
binded strategy object. Data base structure determines the backtesting mode can only
be performed on individual stocks, thus each atomicdispatcher open one subprocess to
run the backtesting.
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""
