import time

start1 = time.time()

dct = {'q': 'w', 'w': 'q', 'e': 'green dog'}

start1 = time.time()

for i in range(10000000):
    if 'r' in dct:
        del dct['r']
    else:
        pass

print('if val in dict: {} seconds'.format(time.time()-start1))

start1 = time.time()

for i in range(10000000):
    try:
        del dct['r']
    except KeyError:
        pass

print('try except: {} seconds'.format(time.time()-start1))