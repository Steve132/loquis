import loquis
import speech_recognition as sr
import sys


def srfilt(words):
	def srfiltword(w):
		if(w.lower() == 'quote'):
			return '"'
		return w
	return [srfiltword(x) for x in words]

def bs(amount):
	sys.stdout.write('\b'*amount)
	sys.stdout.write(' '*amount)
	sys.stdout.write('\b'*amount)
	sys.stdout.flush()

#TODO: Rewrite tokenizer to be streaming tokenizer, so that you can integrate this properly
def get_next_command(r,source):
	command = []
	a=""
	sys.stdout.write(">")
	sys.stdout.flush()
	while(True):
		audio=r.listen(source) # listen for the first phrase and extract it into audio data
		try:
			ht=r.recognize(audio)
		except LookupError:
			continue

		t=srfilt(ht.split())
		last=t[-1].lower()
		command.extend(t)
		if(last=='confirm'):
			command.pop()
			sys.stdout.write("\n")
			return ' '.join(command)
		if(last=='no'):
			command.pop()
			#print(l)
			l=len(command.pop())+1
			#print(l)
			bs(l)
			continue
		if(last=='cancel'):
			command=[]
			sys.stdout.write("\n>")
		if(last=='quit'):
			sys.stdout.write("\n")
			return False
		sys.stdout.write(' '+' '.join(t))
		sys.stdout.flush()
	



if(__name__=='__main__'):
	interp=loquis.Interpreter(language='en',defaultcontext={},verbose=False)
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
			
