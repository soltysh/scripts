#!/usr/bin/python3.4
"""
This script is for controlling Lenovo TouchPad on my laptop.
It uses xinput --list for getting the touchpad's id and then turns if on/off.
"""

import argparse
import re
import subprocess
import sys

def get_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--on', dest='on', action='store_const', const='1', help='Turn TouchPad on.')
	parser.add_argument('--off', dest='on', action='store_const', const='0', help='Turn TouchPad off.')
	parser.set_defaults(on=False)
	return parser

def touchpad_ctrl(args):
	xinput_bytes = subprocess.check_output(['xinput', '--list'])
	xinput_text = xinput_bytes.decode('utf-8')
	match = re.search('PS/2 Synaptics TouchPad.*id=(\d+)', xinput_text)
	if not match:
		return 'No TouchPad id found!'
	touchpad_id = match.group(1)
	subprocess.call(['xinput', 'set-prop', touchpad_id, 'Device Enabled', args.on])

if __name__ == '__main__':
	parser = get_parser()
	if len(sys.argv) < 2:
		parser.print_help()
		sys.exit()
	sys.exit(touchpad_ctrl(parser.parse_args()))
