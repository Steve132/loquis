#!/usr/bin/env python

#This is the loquis reference interpreter
import inspect
from collections import namedtuple
import os,os.path
from functools import partial
import importlib

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
			#todo make the interpreter keep track of its token state for streaming execution
		self.verbose=verbose
		self.language='en'
		self.context['stack']=self.stack.sdata
		self.context['language']=language
		self.context['interpreter']=self
		#load the standard library using the import mechanism
		self.load_python_module('std')
		self._find_modules()

	def run(self,scripttext):
		p=self.parse(scripttext)
		k=self.tokenize(p)
		self.execute(k)

	def load_module(self,modname):
		try:
			self.load_python_module(modname) #check also current directory
		except:
			self.load_loquis_module(modname)
		
		
	def load_python_module(self,modname):
		lang=self.language
	
		m=importlib.import_module('modules.'+modname)
		if('languages' in dir(m) and lang in m.languages):
			importdict=m.languages[lang]
		else:
			importdict={}
			#importdict={}
			#for k,v in dir(m).items():
			#	if(v.importdict[k]=v
		for k,v in importdict.items():
			self.context[k]=v

	def load_loquis_module(self,modname,directory=""):
		fn=os.path.join(directory,modname+'.lq')		
		try:
			t=open(fn).read()
		except:
			raise Exception("Failure to open loquis module "+fn)
		return self.run(t)

	def _find_modules(self):
		thisdir=os.path.dirname(os.path.realpath(__file__))
		moduledir=os.path.join(thisdir,'modules')
		for root, dirs, files in os.walk(moduledir):
			for d in dirs:
				self.load_python_module(d)
			for f in files:
				se=os.path.splitext(f)
				if(se[1]=='.py' and se[0] !='std'):
					self.load_python_module(se[0])
			
	
	def parse(self,text):
		quotegroups=text.split('"')
		wordsout=[]
		for i in range(len(quotegroups)):
			g=quotegroups[i]
			if(i % 2 == 1):
				wordsout.append(g.format()) #TODO figure out control characters
			else:
				wl=reduce(lambda gr,rs: gr.replace(rs,' ; '),['\n',';','.','then',','],g)
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
		i=0
		while(i<len(validwords)):
			w=validwords[i]
			if(w=='procedure'):
				try:
					psize=validwords[i:].index('end')
				except:
					raise "Error, no corresponding 'end' found for procedure!"
				pname=validwords[i+1]
				beginprocedure=i+2
				endprocedure=i+psize
				i+=psize+1
				ptokens=self.tokenize(validwords[beginprocedure:endprocedure])
				self.context[pname]=partial(self.execute,ptokens)
				print(validwords,psize,pname,beginprocedure,endprocedure,i,ptokens)
				continue
				
				
			if(w==';'):
				outw.extend(curst[::-1])
				curst=[]
			else:
				curst.append(w)
			i+=1

		return outw
	def _verbprint(self,s):
		if(self.verbose):
			print(s)

	def execute(self,tokens,context=None,stack=None):
		if(not context):
			context=self.context
		if(not stack):
			stack=self.stack
		#push all tokens on the stack.  Should we look them up contextually first? YES for executing RPN this is REQUIRED 
		#Should also figure out control flow stuff here...function definitions at least and looping...
		i=0;
		while(i<len(tokens)):
			T=tokens[i]
			
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
			i+=1


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
	interp=Interpreter(language='en',fillerstrings=lang.fillerstrings,defaultcontext={},verbose=False)
	if(len(sys.argv) > 1):
		t=interp.load_loquis_module(sys.argv[1])
	else:
		print("Loquis REPL mode: Type 'quit' to exit.")
		quit=False;
		while(not quit):
			t=raw_input(":D>> ")
			if(t=='quit'):
				break
			else:
				interp.run(t)
				
	
