'''text
A file that contains ASCII art representations of alphabets
Includes a dictionary that conveniently stores all characters
An extra character has been included to allow for the wiping
of screens'''

a = '''
 █████    
██   ██   
███████   
██   ██   
██   ██   ''' 

b = '''
██████    
██   ██   
██████    
██   ██   
██████    '''

c = '''
 ██████   
██        
██        
██        
 ██████   '''

d = '''
██████    
██   ██   
██   ██   
██   ██   
██████    '''

e = '''
███████   
██        
█████     
██        
███████   '''

f = '''
███████   
██        
█████     
██        
██        '''

g = '''
 ██████   
██        
██   ███  
██    ██  
 ██████   '''

h = '''
██   ██   
██   ██   
███████   
██   ██   
██   ██   '''

i = '''
████████  
   ██     
   ██     
   ██     
████████  '''

j = '''
     ██   
     ██   
     ██   
██   ██   
 █████    '''

k = '''
██   ██   
██  ██    
█████     
██  ██    
██   ██   '''

l = '''
██        
██        
██        
██        
███████   '''

m = '''
███    ███ 
████  ████ 
██ ████ ██ 
██  ██  ██ 
██      ██'''

n = '''
███    ██ 
████   ██ 
██ ██  ██ 
██  ██ ██ 
██   ████ '''

o = '''
 ██████   
██    ██  
██    ██  
██    ██  
 ██████   '''

p = '''
██████    
██   ██   
██████    
██        
██        '''

q = '''
 ██████   
██    ██  
██    ██  
██    ██  
 ██████   
    ██    '''

r = '''
██████    
██   ██   
██████    
██   ██   
██   ██   '''

s = '''
███████   
██        
███████   
     ██   
███████   '''

t = '''
████████  
   ██     
   ██     
   ██     
   ██     '''

u = '''
██    ██  
██    ██  
██    ██  
██    ██  
 ██████   '''

v = '''
██    ██  
██    ██  
██    ██  
 ██  ██   
  ████    '''

w = '''
██     ██ 
██     ██ 
██  █  ██ 
██ ███ ██ 
 ███ ███  '''

x = '''
██   ██   
 ██ ██    
  ███     
 ██ ██    
██   ██   '''

y = '''
██    ██  
 ██  ██   
  ████    
   ██     
   ██     '''

z = '''
███████   
   ███    
  ███      
 ███      
███████   '''

wipe = '''
██████████
██████████
██████████
██████████
██████████'''


lettersDict = {
 'A' : a, 'B' : b, 'C' : c, 'D' : d, 'E' : e, 'F' : f,
 'G' : g, 'H' : h, 'I' : i, 'J' : j, 'K' : k, 'L' : l, 'M' : m,
 'N' : n, 'O' : o, 'P' : p, 'Q' : q, 'R' : r, 'S' : s, 'T' : t,
 'U' : u, 'V' : v, 'W' : w, 'X' : x, 'Y' : y, 'Z' : z, '#' : wipe
 }