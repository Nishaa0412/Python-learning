'''
The conversion of one data type into the other is called type casting 
1.Explicit
2.Implicit
'''

a= "1"
b= "2"
#a = 1
#b = 2
print( int(a) + int (b))
print(float (a)+ float(b))

# Implicit typecasting
c = 7
print( type (c))
d = 1.4
print(type(d))
e = c + d
print(e)
print(type(e))
 
