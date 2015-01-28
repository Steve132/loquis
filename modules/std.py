import loquis

@loquis.command
def get(key,obj):
	if(isinstance(key,int)):
		return [obj[key]]
	if(hasattr(obj,key)):
		return [getattr(obj,key)]
	return [obj[key]]

@loquis.command
def bottom(count,obj):
	return [obj[-count:]]

@loquis.command
def top(count,obj):
	return[obj[:count]]

@loquis.command
def first(obj):
	return[obj[0]]

@loquis.command
def last(obj):
	return[obj[0]]

def _import(context,stack):		#TODO add filesystem stuff to the import list..#TODO add .lq imports.  #TODO add relative imports
	context['interpreter'].load_module(stack.pop())

#possibly concurrancy using python threads?  Basically spawn an interpreter with a shared context

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

@laquis.command
def nop():
	pass

languages={'en':
	{	'get':get, 
		'element':get,
		'last':last,
		'first':first,
		'top':top,
		'bottom':bottom,
		'where':where, 
		'copy':copy,
		'print':_print,
		'ask':_user_string,
		'_ask':_user_string,
		'import':_import,
		'add':add,
		'so':nop,
		'to':nop,
		'do':nop,
		'my':nop,
		'is':nop,
		'of':nop,
		'in':nop,
		'on':nop,
		'the':nop,
		'result':copy,
		'it':copy,
		'that':copy
	}
}
