import loquis

a="""
languages={'en':{}}

try:
	import auth.google
	import gdata.contacts.data
	import gdata.contacts.client
	
	gd_client=gdata.contacts.client.ContactsClient(source='Loquis-GoogleContactsModule')
	gd_client.ClientLogin(auth.google.username,auth.google.password, gd_client.source)
	contacts=None
	def get_data():
		global contacts
		if(not contacts):
			contacts=[]
			feed = self.gd_client.GetContacts()
			ctr = 0
			while feed:
				for i, entry in enumerate(feed.entry):
					if not entry.name is None:
						family_name = entry.name.family_name is None and " " or entry.name.family_name.text
						full_name = entry.name.full_name is None and " " or entry.name.full_name.text
						given_name = entry.name.given_name is None and " " or entry.name.given_name.text
						print '\n%s %s: %s - %s' % (ctr+i+1, full_name, given_name, family_name)
					else:
						print '\n%s %s (title)' % (ctr+i+1, entry.title.text)
					if entry.content:
					print ' %s' % (entry.content.text)
					for p in entry.structured_postal_address:
					print ' %s' % (p.formatted_address.text)
					# Display the group id which can be used to query the contacts feed.
					print ' Group ID: %s' % entry.id.text
					# Display extended properties.
					for extended_property in entry.extended_property:
					if extended_property.value:
					value = extended_property.value
					else:
					value = extended_property.GetXmlBlob()
					print ' Extended Property %s: %s' % (extended_property.name, value)
					for user_defined_field in entry.user_defined_field:
					print ' User Defined Field %s: %s' % (user_defined_field.key, user_defined_field.value)
					ctr+=len(feed.entry)
				next = feed.GetNextLink()
				feed = None
				if next:
					feed = self.gd_client.GetContacts(uri=next.href)
				else:
					feed = None
		return contacts
	#{}

	@loquis.command
	def contact(query):
		try:	
			
		except Exception as e:
			pass
	languages['en']['contact']=contact
except Exception as e:
	print(e)
	print(__name__+": Can't use google contacts on this machine without proper google auths in auth/google.py")

		"""
