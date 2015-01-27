import loquis
import subprocess

@loquis.command
def run(query,*args):
	return [subprocess.check_output([query]+list(args))]

languages={'en':{'run':run}}
