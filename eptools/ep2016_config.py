
import os.path as op
import socket

hn = socket.gethostname()


ROOT_DIR = ''

# Use the name of my computer to setup local variables and
# hold different configurations.
if hn == 'calm.local':
    # It is a good idea to setup the INKSCAPE_BINPATH for docstamp on Mac computers.
    INKSCAPE_BIN = '/Applications/Inkscape.app/Contents/Resources/bin/inkscape'
    ROOT_DIR     = op.expanduser('~/Dropbox (Personal)/ep15/badge/factory')
    api_key_file = op.expanduser('~/Projects/ep16/google_api_key.json')
elif hn == 'corsair':
    ROOT_DIR     = op.expanduser('~/Dropbox/ep15/badge/factory')
    api_key_file = op.expanduser('~/Projects/ep16/google_api_key.json')

# the ep2016 responses spreadsheet
sponsors_billing_worksheet = ('1Dbxy1a0c-IbXdxVXmbTeU6zE6AKV4N0xKK2GANSw9Mw',
                              'Form responses 1')
