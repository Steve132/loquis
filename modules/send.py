import loquis

languages={'en':{}}

if(loquis.platform_type == 'Desktop'):
	try:
		import auth.twillo
		from twilio.rest import TwilioRestClient 
		twillo_sid=auth.twillo.sid
		twillo_token=auth.twillo.token
		twillo_number=auth.twillo.numbers[0]
		client=TwilioRestClient(twillo_sid,twillo_token)
		def twillo_number_parse(num):
			if(isinstance(num,int)):
				return "+"+str(num)
			else:
				return "+"+filter(lambda x:x.isdigit(),num)
		@loquis.command
		def text(number,bodytext):
			client=TwilioRestClient(twillo_sid,twillo_token)
			client.messages.create(from_=twillo_number_parse(twillo_number),to=twillo_number_parse(number),body=bodytext)
		@loquis.command
		def mms(number,url):
			client=TwilioRestClient(twillo_sid,twillo_token)
			client.messages.create(from_=twillo_number_parse(twillo_number),to=twillo_number_parse(number),media_url=url)
		languages['en']['text']=text
		languages['en']['mms']=mms
	except Exception as e:
		print(e)
		print(__name__+": Can't use texting or sms on this machine without proper twillo auths in auth/twillo.py")

try:
	import auth.email
	import smtplib

	smtp_server_address=auth.email.smtp_server_address
	smtp_server_port=auth.email.smtp_server_port
	smtp_username=auth.email.smtp_username
	smtp_password=auth.email.smtp_password

	@loquis.command
	def send_email(message,to,subject=None,cc=None):
		if(to and not isinstance(to,list)):
			to=[to]
		if(cc and not isinstance(cc,list)):
			cc=[cc]
		try:	
			smtpserver = smtplib.SMTP(smtp_server_address,smtp_server_port)
			smtpserver.ehlo()
			smtpserver.starttls()
			smtpserver.ehlo()
			smtpserver.login(smtp_username, smtp_password)
			from_addr=smtp_username
			header  = 'From: %s\n' % from_addr
			header += 'To: %s\n' % ','.join(to)
			if(cc):
				header += 'Cc: %s\n' % ','.join(cc)
			if(subject):
				header += 'Subject: %s\n\n' % subject
			message = header + message

			problems = smtpserver.sendmail(from_addr, to, message)
			smtpserver.quit()
		except Exception as e:
			print(e)
			raise loquis.LoquisException("Failed to send email")
	languages['en']['mail']=send_email
except Exception as e:
	print(e)
	print(__name__+": Can't use email on this machine without proper smtp auths in auth/smtp.py")

		



