# the modulus of with preceding lower number gives the lower number back
print(8%10)

# modulus can also be used to 'glue' strings and object key values together like so...
x = 'abc_%(key)s_'
x %= {'key':'value'}
print(x) 

x = 'Sir %(Name)s '
x %= {'Name':'Lancelot'}
print(x) 
