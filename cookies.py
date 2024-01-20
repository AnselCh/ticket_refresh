# Ref: https://stackoverflow.com/questions/14742899/using-cookies-txt-file-with-python-requests
# Use this extension: https://chromewebstore.google.com/detail/open-cookiestxt/gdocmgbfkjnnpapoeobnolbbkoibbcif
# to extract your cookies into a file called tixcraft.com_cookies.txt
# It's ok to disable or uninstall the extension once you extract the cookies.

import re
import os.path
    
def parse_cookie_file(cookie_file):
    """
    Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests.
    """

    cookies = {}
    with open (cookie_file, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                line_fields = re.findall(r'[^\s]+', line) #capturing anything but empty space
                try:
                    cookies[line_fields[5]] = line_fields[6]
                except Exception as e:
                    # print (e)
                    # Some fields are not long enough but it is ok to ignore them
                    pass
          
    return cookies

def get_cookies():
    cookies = parse_cookie_file('tixcraft.com_cookies.txt') if os.path.isfile('tixcraft.com_cookies.txt') else dict()
    return cookies