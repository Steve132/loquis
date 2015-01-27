import loquis
import speech_recognition as sr


def srfilt(words):
	def srfiltword(w):
		if(w.lower() == 'quote'):
			return '"'
		return w
	return [srfiltword(x) for x in words]

#TODO: Rewrite tokenizer to be streaming tokenizer, so that you can integrate this properly
def get_next_command(r,source):
	command = []
	a=""
	while(True):
		audio=r.listen(source) # listen for the first phrase and extract it into audio data
		try:
			ht=r.recognize(audio)
			print("Heard: "+ht)
			t=srfilt(ht.split())
			last=t[-1].lower()
			command.extend(t)
			if(last=='confirm'):
				command.pop()
				break
			if(last=='no'):
				command.pop()
				command.pop()
			if(last=='cancel'):
				command=[]
			if(last=='quit'):
				return False
			print(' '.join(command))
			
		except LookupError: # speech is unintelligible
			pass#print("Could not understand audio")
	return ' '.join(command)



if(__name__=='__main__'):
	import languages.en as lang
	interp=loquis.Interpreter(language='en',fillerstrings=lang.fillerstrings,defaultcontext={},verbose=False)
	r = sr.Recognizer()
	with sr.Microphone() as source: # use the default microphone as the audio source
		print("Loquis REPL mode: Say 'quit' to exit.")
		quit=False;
		while(not quit):
			t=get_next_command(r,source)
			if(not t):
				quit=True
				break
			interp.run(t)
			
