# 此方式导入，调用函数时，前面需要加模块名称
# 可以通过 as 取一个别名，取别名后，只能通过别名调用函数
import time as tt
print(tt.time())

# 此方式导入，可以指定部分函数或所有函数，调用时直接调函数名称
from time import *
print(time())