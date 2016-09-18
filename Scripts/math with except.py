#math
import sys
a = 0
b = 30
try:
    c = b/a
    print (c)
    f = open(r'D:\Work\Telebreeze\Scripts\text.txt', 'w')
    f.write(str(c))
    f.close()
except ZeroDivisionError:
    print ("You shouldnt devide by zero")    
    sys.exit("Division by zero")
