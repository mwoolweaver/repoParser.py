from lib.getRepoFile import get, exceptions

import shutil

def getCydiaIcon(repoURL):

    cydiaIcons = [] 
    NCI = []

    for url in repoURL:
        cydiaIconURL = url + "/CydiaIcon.png"
        try:
            checkCydiaIcon = get(cydiaIconURL, headers={"User-Agent":"Debian APT-HTTP/1.3 (2.1.10)"}, stream=True)

            if checkCydiaIcon.status_code == 200:
                
                checkCydiaIcon.raw.decode_content = True
                fileToSaveTo = "CydiaIcon/" + str(repoURL.index(url)) + ".CydiaIcon.png"
        
                with open(fileToSaveTo, 'wb') as f:
                    shutil.copyfileobj(checkCydiaIcon.raw, f)
                
                cydiaIcons.append([cydiaIconURL, repoURL.index(url)])
                print ('\033[K  {0} Found {1} CydiaIcon.png {2}\r'.format((repoURL.index(url)+1), url, checkCydiaIcon.status_code), end='')
            else:
                print ('\033[K  {0} Failed to find {1} CydiaIcon.png {2}\r'.format((repoURL.index(url)+1), url, checkCydiaIcon.status_code), end='')
                NCI.append([url, checkCydiaIcon.status_code])
        
        # Repo can't be found
        except exceptions.Timeout as err:
            print ('\033[K  {0} CydiaIcon.png not Found!!! {1}, 404\r'.format((repoURL.index(url)+1), url), end='')
            NCI.append([url, err])
            continue # start the loop over and try the next repo.
        # Repo can't be found
        except exceptions.ConnectionError as err:
            print ('\033[K  {0} CydiaIcon.png not Found!!! {1}, 404\r'.format((repoURL.index(url)+1), url), end='')
            NCI.append([url, err])
            continue # start the loop over and try the next repo.
        # will exit loop instead of killing the script
        except KeyboardInterrupt:
            break

    return (cydiaIcons, NCI)
