import sys
import httplib, urllib

HTTP_POST_HEADERS = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
# TODO Add time stamp correctly
MESSAGES = [ \
            ('Report Every 5 seconds', "AT+GTTRI=gl100,0000,2359,1,5,20100101120000"), \
            ('Report every 60 seconds', "AT+GTTRI=gl100,0000,2359,1,60,20100101120000"), \
            ('Report every 15 minutes', "AT+GTTRI=gl100,0000,2359,15,900,20100101120000"), \
            ('Stop reporting', "AT+GTTRI=gl100,0000,0001,1,120,20100101120000"), \
            ('Check battery', "AT+GTRTO=gl100,A,20100101120000"), \
            ('Set vehicle mode', "AT+GTSFR=gl100,1,1,1,1,1,15,200,0,0,20100611123832"), \
            ('Set walking mode', "AT+GTSFR=gl100,1,1,1,1,1,2,100,0,0,20100611123722"), \
            ('Reboot device', "AT+GTRTO=gl100,3,20100101120000"), \
            ('Locate device now', "AT+GTRTO=gl100,1,20100101120000") \
            ]
def main():
    args = sys.argv[1:] # First argument is always file name
    if len(args) != 4: # Check we've got the right number of arguments
        print "sorry, you need to enter in 'account password phone' as arguments"
        sys.exit(1)
    parameters = ['account', 'password', 'phone', 'send_url']
    params = dict(zip(parameters, args)) # No error checking here - just matching up the parameters to the arguments

    conn = httplib.HTTPConnection(params['send_url'], 80) # Set up a connection to meercom
    while(1):
        choice = -1
        for i, value in enumerate(MESSAGES):
            print i, value[0]
        try: 
            print "="*50
            choice = int(raw_input('Choose an option: '))
        
        except: choice = -1
        if choice < len(MESSAGES) and choice > -1:
            params['message'] = MESSAGES[choice][1]
            print "Sending message: " + params['message'] + " to: " + params['phone']
            url_params = urllib.urlencode(params)
            conn.request("POST", "/sendsms.asp", url_params, HTTP_POST_HEADERS)
            response = conn.getresponse()
            print response.status, response.reason, response.read()
        else: 
            print "="*50
            print "Sorry, that option isn't valid try again"


if __name__ == '__main__':
    main()
