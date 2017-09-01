"""
Backtest using "StrategyExample.py"
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""
from Dataloader.dispatcher import *
from Strategy.StrategyExample import *

if __name__ == "__main__":
    dispatcher = Dispatcher("E:/QuantFrameWork/BeaCon/Dataloader/backtestconfig.json")
    strategy = TestStrat()
    strategy.setdispatcher(dispatcher)