from optparse import OptionParser 
parser = OptionParser() 

add_option = parser.add_option
options = None
args = None

def option():
	global options
	global args
	if None == options:
		(options, args) = parser.parse_args() 
	return options

DEFINE_FLAG = add_option
FLAG = option

"""
if options.pdcl==True: 
    print 'pdcl is true' 
if options.zdcl==True: 
    print 'zdcl is true' 
"""

DEFINE_FLAG(    "-m", "--my_flag",
                action="store_true", 
                dest="my_flag", default=False, 
                help="Whether to show tag-itemlist") 

def main():
    print option().my_flag
        

if __name__ == '__main__':
    main()
