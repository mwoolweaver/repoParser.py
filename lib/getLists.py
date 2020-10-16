from requests import get, exceptions

def getLists():

    LBC = []
    LBCD = []
    WILBC = []
    DILBC = []

    defaultRepos = ["http://cydia.zodttd.com/repo/cydia", "http://apt.modmyi.com", "http://apt.thebigboss.org/repofiles/cydia", "https://apt.bingner.com", "http://apt.saurik.com", "http://apt.thebigboss.org", "https://apt.procurs.us", "https://repo.packix.com", "https://repo.dynastic.co", "https://repounclutter.coolstar.org", "https://repo.theodyssey.dev", "https://repo.chariz.com", "https://checkra.in/assets/mobilesubstrate", "https://repo.chimera.sh"]
    reposWithIssues = ["https://www.5781000.co/dcrm", "https://ios.jeffsjunk.co.uk", "https://repo.sciency.us", "https://wizage.github.io/repo/", "https://iluwqaa.github.io/", "https://booleanmagic.com/repo", "https://cydiamy.github.io/1.0.4", "https://chickenmatt5.github.io/repo", "https://iamjamieq.github.io/repo", "http://rcrepo.com", "https://bandarhl.github.io", "https://xninja.xyz/apt", "https://apt.xninja.xyz", "https://coolstar.org/publicrepo"]

    try: # to GET list from api.ios-repo-updates.com
        getIRU = get("https://api.ios-repo-updates.com/1.0/popular-repos/")
        if getIRU.status_code == 200:
            jsonIRU = getIRU.json()
            IRU = jsonIRU
            # check ios-repo-updates.com add to listBeforeCheck[] if duplicate add to listBeforeCheckDUP[]
            for repoIRU in IRU:
                lbc1 = repoIRU["url"].rstrip('/')
                lbc1strip = lbc1.lstrip()

                if lbc1strip not in defaultRepos:
                    if lbc1strip not in reposWithIssues:
                        if lbc1strip not in LBC:
                            LBC.append(lbc1strip)
                        else: # is dup so save to listBeforeCheckDUP[]
                            LBCD.append(lbc1strip)
                    else:
                        WILBC.append(lbc1strip)
                else: 
                    DILBC.append(lbc1strip)     
        else:
            print ('Can not find https://api.ios-repo-updates.com/1.0/popular-repos/ {0}\r'.format(getIRU.status_code))
    # can not find https://api.ios-repo-updates.com/1.0/popular-repos/
    except exceptions.Timeout as err:
        print ('Can not find https://api.ios-repo-updates.com/1.0/popular-repos/ {0}\r'.format(err))
    # can not find https://api.ios-repo-updates.com/1.0/popular-repos/
    except exceptions.ConnectionError as err:
        print ('Can not find https://api.ios-repo-updates.com/1.0/popular-repos/ {0}\r'.format(err))

    try: # to GET list from api.parcility.co
        getParcility = get("https://api.parcility.co/db/repos/small")
        jsonParcility = getParcility.json()
        if jsonParcility["code"] == 200:
            parcility = jsonParcility["data"]
            # check parcility.co agaianst add to listBeforeCheck[] if duplicate add to listBeforeCheckDUP[]
            for repoParcility in parcility:
                lbc2 = repoParcility["url"].rstrip('/')
                lbc2strip = lbc2.lstrip()
                if lbc2strip not in defaultRepos:
                    if lbc2strip not in reposWithIssues:
                        if lbc2strip not in LBC:
                            LBC.append(lbc2strip)
                        else: # is dup so save to listBeforeCheckDUP[]
                            LBCD.append(lbc2strip)
                    else:
                        WILBC.append(lbc2strip)
                else: 
                    DILBC.append(lbc2strip)
        else:
            print ('Can not find https://api.parcility.co/db/repos/small {0}\r'.format(jsonParcility["code"]))
    # can not find https://api.parcility.co/db/repos/small
    except exceptions.Timeout as err:
        print ('Can not not find https://api.parcility.co/db/repos/small {0}\r'.format(err))
    # can not find https://api.parcility.co/db/repos/small
    except exceptions.ConnectionError as err:
        print ('Can not not find https://api.parcility.co/db/repos/small {0}\r'.format(err))

    if getIRU.status_code != 200 and jsonParcility["code"] != 200:
        print (" ")
        print ("we can't fetch our list so we must quit.")
        raise SystemExit
    
    return (LBC, LBCD, WILBC, DILBC)