## Algorithm Trading

Neural networks, machine learning, regressions, alogrithms based on bollinger bands, SMAs and momentum/contrarian strategies

https://github.com/kurumbus/algorithmic-trading/blob/master/interactive-brokers-sma.ipynb - a script which trades on Interactive Brokers using Simple Moving Averages. If you think it's too easy to be profitable - you're right.  


https://github.com/kurumbus/algorithmic-trading/blob/master/momentum-contrarian-opt.ipynb  - Attempt to optimize parameters for momentum/contrarian strategies.
Obviously if you play with numbers long enough, you can create an illusion of profitability. But median is obviously -10% 
![2024-08-27_18h32_08.png](images%2F2024-08-27_18h32_08.png)


https://github.com/kurumbus/algorithmic-trading/blob/master/bollinger-bands.ipynb - Good old Bollinger Bands
![bollinger.png](images%2Fbollinger.png)

The  strategy produces net 1% in 6 years. Still better than your portfolio
![bollinger-results.png](images%2Fbollinger-results.png)

https://github.com/kurumbus/algorithmic-trading/blob/master/DNNModel.py  Training a sequential Keras Model 

https://github.com/kurumbus/algorithmic-trading/blob/master/classification.ipynb  - Simple Machine Learning Algorithm using scikit logistics regression
Produces 600% of profit on training set:
![2024-08-27_20h54_01.png](images%2F2024-08-27_20h54_01.png)
On real data... Not so much:
![2024-08-27_20h55_13.png](images%2F2024-08-27_20h55_13.png)
But it's regression, what do you want.

https://github.com/kurumbus/algorithmic-trading/blob/master/linear-regression-scikit.ipynb - Simple Linear Regression with scikit
Can previous day returns predict today's market? Nah, not really
![2024-08-27_20h56_21.png](images%2F2024-08-27_20h56_21.png)

https://github.com/kurumbus/algorithmic-trading/blob/master/neural-network-tensorflow.ipynb - a tensorflow neural network trying to use one-minute bars to find profitable opportunities. 
Let's just say for now it can't find them.
![2024-08-27_20h58_08.png](images%2F2024-08-27_20h58_08.png)

https://github.com/kurumbus/algorithmic-trading/blob/master/neural-network-ibkr.ipynb  - a working implementation of a neural network trading on IBKR (Interactive Brokers).
