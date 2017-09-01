"""
Backtest using "StrategyExample.py"
Success on backtesting, next step will focus on logging and outcome production!!
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""
from Dataloader.dispatcher import *
from Strategy.StrategyExample import *

if __name__ == "__main__":
    dispatcher = Dispatcher("E:/QuantFrameWork/BeaCon/Dataloader/backtestconfig.json")
    strategy = TestStrat("E:/QuantFrameWork/BeaCon/Strategy/Config/strategyconfig.json")
    strategy.setdispatcher(dispatcher)
    dispatcher.loaddata()
    dispatcher.run()