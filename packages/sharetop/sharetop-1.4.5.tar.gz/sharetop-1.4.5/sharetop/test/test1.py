from sharetop.core.stock import get_real_time_data
import time
stock_code = '562510'
# stock_code = '516880'
# stock_code = '002714'
# stock_code = '600809'
start = int(time.time())
h = get_real_time_data(stock_code)
end = int(time.time())
t = end - start
print('t:', t)
print(h)
d = h.to_dict("records")
print("d:", d)

