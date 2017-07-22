import img_name
import sys
help = """
Usage Syntax: python image_search.py [agrument] [String Content]
Options:

Positional Arguments:
--url : To get the name from url of the image file.

--img : To get the name from path of image file from system.

--help: Show this help message and exit.
       """
invalid_syntax = """Use --help option for usage syntax. """
invalid_option = """Use --help for usage options and syntax. """
try:
    if sys.argv[1] == '--url':
        print(img_name.name_from_url(sys.argv[2]))
        sys.exit()
    if sys.argv[1] == '--img':
        print(img_name.name_from_image(sys.argv[2]))
        sys.exit()
    if sys.argv[1] == '--help':
        print(help)
        sys.exit()
    if len(sys.argv) == 0 or len(sys.argv[2]) == 0:
        print(invalid_syntax)
        raise ValueError('Invalid Syntax')
        sys.exit()
    else:
        print(invalid_option)
        raise ValueError('Invalid Options')
        sys.exit()
except IndexError:
    print(invalid_syntax)
    sys.exit()