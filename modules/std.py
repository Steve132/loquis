import loquis
import importlib

@loquis.command
def get(key,obj):
	if(isinstance(key,int)):
		return [obj[key]]
	if(hasattr(obj,key)):
		return [getattr(obj,key)]
	return [obj[key]]

@loquis.command
def last(count,obj):
	return [obj[-count:]]

@loquis.command
def first(count,obj):
	return[obj[:count]]

@loquis.command
def top(obj):
	return[obj[0]]

def _import(context,stack):		#TODO add filesystem stuff to the import list..#TODO add .lq imports.  #TODO add relative imports
	lang=context['language']
	modname=stack.pop()
	
	m=importlib.import_module('modules.'+modname)
	if('languages' in dir(m) and lang in m.languages):
		importdict=m.languages[lang]
	else:
		importdict={}
		#importdict={}
		#for k,v in dir(m).items():
		#	if(v.importdict[k]=v
	for k,v in importdict.items():
		context[k]=v

@loquis.command
def _user_string(query):
	return [raw_input(query)]

@loquis.command
def add(a,b):
	return [a+b]

@loquis.command
def where(key,value):
	return [loquis.Where(key=key,value=value)]

@loquis.command
def copy(val,repeats=2):
	return [val]*repeats
@loquis.command
def length(val):
	return len(val)

@loquis.command
def _print(val):
	print(val)

languages={'en':
	{	'get':get, 
		'element':get,
		'last':last,
		'first':first,
		'top':top,
		'where':where, 
		'copy':copy,
		'print':_print,
		'ask':_user_string,
		'import':_import,
		'add':add
	}
}
