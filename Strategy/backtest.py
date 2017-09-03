"""
Backtest using "StrategyExample.py"
Success on backtesting, next step will focus on logging and outcome production!!
moduleaurther : Wang Wei <wangwei_aperion@163.com>
"""
from Dataloader.dispatcher import *
from Strategy.StrategyExample import *
from Strategy.StrategyExample2 import *
import logging
import os
import shutil

if __name__ == "__main__":
    #########Clear Logging File##########
    shutil.rmtree("E:/QuantFrameWork/BeaCon/Logging")
    os.mkdir("E:/QuantFrameWork/BeaCon/Logging")
    shutil.rmtree("E:/QuantFrameWork/BeaCon/Strategy/temp")
    os.mkdir("E:/QuantFrameWork/BeaCon/Strategy/temp")
    ######### Logging Purpose ##########
    mainlogger = logging.getLogger("Main")
    mainlogger.setLevel(logging.INFO)
    mainhandler = logging.FileHandler("E:/QuantFrameWork/BeaCon/Logging/main.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    mainhandler.setFormatter(formatter)
    mainlogger.addHandler(mainhandler)
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.INFO)
    streamhandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(message)s'))
    mainlogger.addHandler(streamhandler)
    ######### Main Strategy ############
    dispatcher = Dispatcher("E:/QuantFrameWork/BeaCon/Dataloader/backtestconfig.json")
    mainlogger.info("Create Dispatcher")
    strategy = TestStrat("E:/QuantFrameWork/BeaCon/Strategy/Config/strategyconfig.json")
    strategy2 = Test2Strat("E:/QuantFrameWork/BeaCon/Strategy/Config/strategyconfig2.json")
    mainlogger.info("Create teststrategy")
    strategy.setdispatcher(dispatcher)
    strategy2.setdispatcher(dispatcher)
    mainlogger.info("Connect dispacther and teststrategy")
    dispatcher.loaddata()
    mainlogger.info("Loading Data Successfully")
    dispatcher.run()
    strategy.end()
    strategy2.end()
    mainlogger.info("Finish Backtesting")
