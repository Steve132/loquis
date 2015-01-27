#!/usr/bin/env python

#This is the loquis reference interpreter
import inspect
from collections import namedtuple
import modules.std 

class Stack(object):
	def __init__(self):
		self.sdata=[]
		
	def push(self,x):
		self.sdata.append(self.filt(x))
	def pop(self):
		return self.sdata.pop()
	def peek(self,index=-1):
		return self.sdata[-1]

	def extend(self,lst):
		self.sdata.extend([self.filt(x) for x in lst])

	def filt(self,x):
		try:
			return int(x)
		except:
			return x
	def __str__(self):
		return str(self.sdata)
	def __len__(self):
		return len(self.sdata)

Where=namedtuple('Where',['key','value'])
class Interpreter(object):
	def __init__(self,language='en',fillerstrings=[],defaultcontext={},verbose=False):
		self.fillerstrings=fillerstrings
		self.context=defaultcontext
		self.stack=Stack()
		self.verbose=verbose
		self.language='en'
		self.context['stack']=self.stack.sdata
		self.context['language']=language
		#bootstrap the standard library using the import mechanism in the standard library
		self.load_module('std')

		
	def load_module(self,modname):
		self.stack.push(modname)
		modules.std._import(self.context,self.stack)
	
	def parse(self,text):
		quotegroups=text.split('"')
		wordsout=[]
		for i in range(len(quotegroups)):
			g=quotegroups[i]
			if(i % 2 == 1):
				wordsout.append(g.format()) #TODO figure out control characters
			else:
				wl=reduce(lambda gr,rs: gr.replace(rs,' ; '),[';','.','then',','],g)
				#g=g.replace(';',' ; ')
				#g=g.replace('.',' ; ')
				#g=g.replace('then',' ; ');
				#g=g.replace(',',' ; ');
				wordsout.extend(wl.split())
	
		validwords=filter(lambda w: w not in self.fillerstrings,wordsout)
		return validwords

	def tokenize(self,validwords):
		validwords.append(';')  #always has a semicolon for find.
	
		outw=[]
		curst=[]
		for w in validwords:
			if(w==';'):
				outw.extend(curst[::-1])
				curst=[]
			else:
				curst.append(w)
		return outw
	def _verbprint(self,s):
		if(self.verbose):
			print(s)

	def execute(self,tokens):
		context=self.context
		stack=self.stack
		#push all tokens on the stack.  Should we look them up contextually first? YES for parsing.  
		#Should also figure out control flow stuff here...function definitions at least and looping...
		for T in tokens:
			self._verbprint("Now processing"+T)
			if(T.lower() in context):
				n=T.lower()
				T=context[T.lower()]
				self._verbprint("Assuming '"+n+"' means "+str(T))
		
			if(hasattr(T, '__call__')):
				retval=T(context=context,stack=stack)
				if(retval):
					if(not isinstance(retval,list)):
						retval=[retval]
					stack.extend(retval)
			else:
				stack.push(T)
	
			self._verbprint(stack)



#all loquis ops are defined to return a list...this is a decorator
def command(f):
	aspec=inspect.getargspec(f)
	args=aspec[0]
	varargs=aspec[1]
	kwargs=aspec[2]
	defaults=aspec[3]	#todo: doesn't handle defaults I don't think
	
	def func(context,stack):
		#todo: how greedy is kwargs?		
		na=0
		cargs=[]
		kwargs={}
		while(len(stack) > 0 and na < len(args)):
			s=stack.pop()
			if(isinstance(s,Where)):
				kwargs[s.key]=s.value
			else:
				cargs.append(s)
			na+=1
		if(varargs):
			cargs.extend(stack.sdata[::-1])
		r=f(*cargs,**kwargs)
		stack.extend(r if r else [])
		return []
	func.is_loquis_command=True;
	return func


if(__name__=="__main__"):
	import languages.en as lang
	import sys
	interp=Interpreter(language='en',fillerstrings=lang.fillerstrings,defaultcontext={})
	#tests
	#t="Get my map destination then email it to Steve"
	#t="copy ducks where repeats is 10, then print stack"
	if(len(sys.argv) > 1):
		t=open(sys.argv[1]).read()
	else:
		t=raw_input()
	p=interp.parse(t)
	k=interp.tokenize(p)
	interp.execute(k)
	
