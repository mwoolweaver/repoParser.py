from lib.getRepoFile import getRepoFile, exceptions
import re


def getRelease (LBC):

    RFLAC = []
    NFR =[]

    for repo in LBC:
        # create URLs for the files we need
        # a Release and a Packages.(zst|xz|lzma|bz2|gz)
        checkReleaseURL = repo + "/Release" # checkRelease[0]

        try: # to GET those endpoints (URLs)
            checkRelease = getRepoFile(checkReleaseURL)
            # IF we find a Release file and a Packages.(zst|xz|lzma|bz2|gz)
            if checkRelease[1] == 200:
                RFLAC.append([repo, checkRelease[0].content])
                print ('\033[K  {0} Found {1} Release {2}\r'.format((LBC.index(repo)+1), repo, checkRelease[1]), end='')
            # IF No Release found
            elif checkRelease[1] != 200:
                print ('\033[K  {0} Release Not Found {1}, {2}\r'.format((LBC.index(repo)+1), repo, checkRelease[1]), end='')
                NFR.append([repo, checkRelease[1]])
            else: # we have a problem
                print ('\033[K  {0} Something is wrong!!!! {1}, {2}\r'.format((LBC.index(repo)+1), repo, checkRelease[1]), end='')
                raise KeyboardInterrupt
        # Repo can't be found
        except exceptions.Timeout as err:
            print ('\033[K  {0} Repo not Found!!! {1}, 404\r'.format((LBC.index(repo)+1), repo), end='')
            NFR.append([repo, err])
            continue # start the loop over and try the next repo.
        # Repo can't be found
        except exceptions.ConnectionError as err:
            print ('\033[K  {0} Repo not Found!!! {1}, 404\r'.format((LBC.index(repo)+1), repo), end='')
            NFR.append([repo, err])
            continue # start the loop over and try the next repo.
        # will exit loop instead of killing the script
        except KeyboardInterrupt:
            break
    return (RFLAC, NFR)
    
def findDUPrelease(LBC):

    release = getRelease(LBC)

    RFLAC = release[0]
    NFR = release[1]

    notDupRelease = []
    notDupURL = []
    isDupURL = []
    isDupRelease = []
    notValidRelease = []
    oldGH = []
    oldGL = []
    oldAS = []
    oldHTTP = []
    notChanged = []

    word = b'Origin:'
    # Check for duplicate Release files
    for file in RFLAC:
        if word in file[1]:
            if file[1] not in notDupRelease:
                notDupURL.append(file[0]); notDupRelease.append(file[1])
            else:
                isDupURL.append(file[0]); isDupRelease.append(file[1])
        else:
            notValidRelease.append(file)

    for dupRelease in isDupRelease:
        # find the duplicate release file index in each list
        indexND = notDupRelease.index(dupRelease)
        indexID = isDupRelease.index(dupRelease)
        # check IF isDupRelease is duplicate because of a github.io URL
        if bool(re.search(r'\b(\.github\.io)\b', notDupURL[indexND])):
            oldGH.append([notDupURL[indexND], isDupURL[indexID]]) # save old URLs
            notDupURL[indexND] = isDupURL[indexID] # set correct url
            notDupRelease[indexND] = isDupRelease[indexID] # set correct Release file
        # check IF isDupRelease is duplicate because of a gitlab.io URL
        elif bool(re.search(r'\b(\.gitlab\.io)\b', notDupURL[indexND])):
            oldGL.append([notDupURL[indexND], isDupURL[indexID]]) # save old URLs
            notDupURL[indexND] = isDupURL[indexID] # set correct url
        # check IF isDupRelease is duplicate because of a appspot.com URL
        elif bool(re.search(r'\b(\.appspot\.com)\b', notDupURL[indexND])):
            oldAS.append([notDupURL[indexND], isDupURL[indexID]]) # save old URLs
            notDupURL[indexND] = isDupURL[indexID] # set correct url
        # check IF isDupRelease is duplicate because of a http URL
        elif bool(re.search(r'(http\:\/\/)', notDupURL[indexND])):
            oldHTTP.append([notDupURL[indexND], isDupURL[indexID]]) # save old URLs
            notDupURL[indexND] = isDupURL[indexID] # set correct url
        else: # not changed
            notChanged.append([notDupURL[indexND], isDupURL[indexID]])

    return (notDupRelease, notDupURL, isDupURL, isDupRelease, notValidRelease, NFR, oldAS, oldGH, oldGL, oldHTTP, notChanged)