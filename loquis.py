#This is the loquis reference interpreter

import languages.en as language

def parse(text):
	quotegroups=text.split('"')
	wordsout=[]
	for i in range(len(quotegroups)):
		g=quotegroups[i]
		if(i % 2 == 1):
			wordsout.append(g)
		else:
			wl=reduce(lambda gr,rs: gr.replace(rs,' ; '),[';','.','then',','],g)
			#g=g.replace(';',' ; ')
			#g=g.replace('.',' ; ')
			#g=g.replace('then',' ; ');
			#g=g.replace(',',' ; ');
			wordsout.extend(wl.split())
	
	validwords=filter(wordsout,lambda w: w not in language.filler)
	return validwords

def tokenize(validwords):
	validwords.append(';')  #always has a semicolon for find.
	first=0
	last=0;

	while(last != (len(validwords)-1))
		last=validwords.index(';')		
		validwords[first:(last+1)]=validwords[last:(first-1):-1]
		first=last+1

	return validwords

def execute(tokens,context={},stack=[]):
	#push all tokens on the stack.
	stack.extend(tokens)

	while(len(stack) > 0)):
		T=stack.pop()
	
		if(T.lower() in context):
			T=context[T.lower()]
		
		if(hasattr(T, '__call__')):
			retval=T(context=context,stack=stack)
			if(retval):
				stack.append(retval)
		else:
			break	#if the top of the stack is not callable, no execution can take place.  Done with this execution iteration



