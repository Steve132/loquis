import loquis

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

def _import(context,stack):		#add filesystem stuff to the import list
	pass

@loquis.command
def _user_string(query):
	return [raw_input(query)]

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

