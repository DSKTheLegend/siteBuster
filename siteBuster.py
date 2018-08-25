import socket
import optparse
import requesocks


def siteBurst(url,wordlist,status_code,verbose):
    
    fhandle = open(wordlist,'r')
    words =  fhandle.read().split()
    dir_found = list()
    # Extentions of most of the web languages included here 
        ## ASP    ## CSS    ## Coldfusion    ## Erlang    ## Flash
        ## HTML   ## Java   ## Javascript    ## Perl      ## PHP
        ## Pthon  ## Ruby   ## SSI           ## XML
        ## Few Others ...
    #extention = ['','.asp','.aspx','.axd','.asx','.asmx','.ashx','.cfm','.css','.yaws','.swf','.html','.htm','.xhtml','.jhtml','.jsp','.jspx','.wss','.do','.action','.js','.pl','.php','.php4','.php3','.phtml','.py','.rb','.rhtml','.shtml','.xml','.rss','.svg','.cgi','.dll']
    #Keeping only commonly found extentions 
    extention = ['','.asp','.aspx','.css','.html','.htm','.jsp','.jspx','.js','.php','.php4','.php3','.xml']    
    false_check = False # a flag to check if we are gettinng false positives or not 
    for word in words:
        false_positive = 0   # a flag to count the number of extentions work for a single word phrase
        for ext in extention :
            req = requesocks.get(url+word+ext) # format -> [http://example.com][index][.html]
            code = req.status_code
            if str(code) in status_code.split(','): # if the site sends a positive response code
                
                print('')
                
                                   
                if ext == '':   #directory file
                    false_positive = false_positive + 1
                    print("# ******** # "+url+word+ext + " directory found !")
                    print('')
                else :  #non-directory file
                    false_positive = false_positive + 1
                    print("#==========# "+url+word+ext + " found !")
                    print('')
                if false_check is False:
                    if false_positive > 4:
                        print("We may be getting false positive results!.")
                        print("Please check the above links manually and tell if those links are valid or not.")
                        user_check = raw_input("Are the links valid ? (yes/no) :")
                        print user_check
                        print type(user_check)
                        if user_check.lower() == "yes":
                            false_check = True
                        else:
                            print("Sorry, please try to check for response codes manually and then provide them using -s <response codes>")
                            quit()
            else :   # if the site sends a negative response code
                if bool(verbose) == True:
                    print("=# "+url+word+ext + " not found !")
                else:    
                    continue
                

def checker(url,port,wordlist,status_code,verbose):
    #Checking is Site is alive or not
    mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s_post = url.find("://")
        host = url[s_post+3:len(url)-1]
        mysock.connect((host,port))
        print("Host : "+host+" is Up!!")
        if port is not 80:
            url = url[:len(url)-1]+":"+str(port)+'/'  
    except:
        print("Host : "+host+" is Down !!")
        quit()
    mysock.close()    
    #Checking if wordlist file exists or not    
    try: 
        
        fhandle = open(wordlist,'r')
        print("Wordlist : "+wordlist+" Found!")
        print("We have "+str(len(fhandle.read().split())*len(status_code))+" combinations to try!")
    except:
        print ("The file you provided : " + wordlist + " is not valid. Please check the path or filename and try again")  
        quit(0)
        
    siteBurst(url,wordlist,status_code,verbose)  
        
def main():
    parser = optparse.OptionParser('usage: siteBuster.py ' + '-u <siteurl> -w <wordlist> [[-p <port>][-s <response code>][-v]')
    parser.add_option('-u', dest='url',type='string',help='enter the url of the site you want to burst')
    parser.add_option('-p', dest='port',type='string',help='enter the port(if site is running on any port other than 80)')
    parser.add_option('-w', dest='wordlist',type='string',help='enter the path of the wordlist you want to use')
    parser.add_option('-s', dest='status_code',type='string',help='enter response codes for which you want to verify (default is [200,204,301,302,307])')
    parser.add_option('-v', dest='verbose',type='string',nargs=0,help='verbose',)
    (options,args) = parser.parse_args()
    
    # url and wordlist are compulsory
    if (options.url == None) | (options.wordlist == None):
        print parser.usage
        exit(0)
    else:
        # assigning url
        url = options.url
        # assigning wordlist
        wordlist = options.wordlist
        #assigning port
        if options.port:
            port = options.port
        else:
            port = 80   #default port
        #assigning response code    
        if options.status_code:
            status_code = options.status_code
        else:
            status_code = "200,204,301,302,307" #default response codes    
        if options.verbose == None :
            verbose = False
        else:
            verbose = True    
                
    if not url.startswith("http"): # if user enters ip or just site name
        url = "http://"+url         
    if not url.endswith('/'):   # just a check
        url = url+'/'
    port = int(port)  
    print("Bursting The Site : " +url)
    checker(url,port,wordlist,status_code,verbose)

if __name__ == '__main__':
    welcome = """
         SSS    iii   TTTTT  EEEE        BBB    U   U   SSS   TTTTT  EEEE   RRRR
        S        I      T    E           B  B   U   U  S        T    E      R   R
        SSSS     I      T    Eee    ###  BBBB   U   U  SSSS     T    Eee    RrrR
            S    I      T    E           B   B  U   U      S    T    E      R   R   
        SSSS   IIIII    T    EEEEEE      BBBB    UUU   SSSS     T    EEEEEE R    R
                                                                           
                                                                               by TheLegend
    """
    print(welcome)
    main()
