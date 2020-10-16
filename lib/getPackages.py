from lib.getRepoFile import getRepoFile, exceptions

from bz2 import decompress as bz2Decompress
from gzip import decompress as zlibDecompress
from lzma import decompress as lzmaDecompress
import zstd

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def getPackages(notDupURL, notDupRelease):

    packagesFilesLAC = []
    NFP = []


    for repo in notDupURL:
        # create URLs for the files we need
        # a Release and a Packages.(zst|xz|lzma|bz2|gz)
    
        checkPackagesURLzst = repo + "/Packages.zst" # checkPackages[0]
        checkPackagesURLxz = repo + "/Packages.xz" # checkPackages[1]
        checkPackagesURLlzma = repo + "/Packages.lzma" # checkPackages[2]
        checkPackagesURLbz2 = repo + "/Packages.bz2" # checkPackages[3]
        checkPackagesURLgz = repo + "/Packages.gz" # checkPackages[4]
        checkPackagesURL = repo + "/Packages" # checkPackages[5]

        try: # to GET those endpoints (URLs)
            
            checkPackages = (getRepoFile(checkPackagesURLzst), getRepoFile(checkPackagesURLxz),\
             getRepoFile(checkPackagesURLlzma), getRepoFile(checkPackagesURLbz2), getRepoFile(checkPackagesURLgz), getRepoFile(checkPackagesURL))
            
            # IF we find a Release file and a Packages.(zst|xz|lzma|bz2|gz)
            if checkPackages[0][1] == 200: # if Packages.zst
                print ('\033[K  {0} Found {1} Release and Packages.zst {2}\r'.format((notDupURL.index(repo)+1), repo, checkPackages[0][1]), end='')
                packagesFilesLAC.append([repo, zstd.uncompress(checkPackages[0][0].content), r''])

            elif checkPackages[1][1] == 200: # if Packages.xz
                print ('\033[K  {0} Found {1} Packages.xz {2}\r'.format((notDupURL.index(repo)+1), repo, checkPackages[1][1]), end='')
                packagesFilesLAC.append([repo, lzmaDecompress(checkPackages[1][0].content), r''])

            elif checkPackages[2][1] == 200: # if Packages.lzma
                print ('\033[K  {0} Found {1} Packages.lzma {2}\r'.format((notDupURL.index(repo)+1), repo, checkPackages[2][1]), end='')
                packagesFilesLAC.append([repo, lzmaDecompress(checkPackages[2][0].content), r''])

            elif checkPackages[3][1] == 200: # if Packages.bz2
                print ('\033[K  {0} Found {1} Packages.bz2 {2}\r'.format((notDupURL.index(repo)+1), repo, checkPackages[3][1]), end='')
                packagesFilesLAC.append([repo, bz2Decompress(checkPackages[3][0].content), r''])

            elif checkPackages[4][1] == 200: # if Packages.gz
                print ('\033[K  {0} Found {1} Packages.gz {2}\r'.format((notDupURL.index(repo)+1), repo, checkPackages[4][1]), end='')
                packagesFilesLAC.append([repo, zlibDecompress(checkPackages[4][0].content), r''])

            elif checkPackages[5][1] == 200: # if Packages
                print ('\033[K  {0} Found {1} Packages {2}\r'.format((notDupURL.index(repo)+1), repo, checkPackages[5][1]), end='')
                packagesFilesLAC.append([repo, checkPackages[5][0].content, r''])

            else: # we have a problem
                print ('\033[K  {0} Something is Wrong!!! {1}, {2}, {3}, {4}, {5}, {6}, {7}\r'.format((notDupURL.index(repo)+1), repo,  checkPackages[0][1], checkPackages[1][1], checkPackages[2][1], checkPackages[3][1], checkPackages[4][1], checkPackages[5][1]), end='')
                raise KeyboardInterrupt
    
        # Repo can't be found
        except exceptions.Timeout as err:
            print ('\033[K  {0} Packages not Found!!! {1}, 404\r'.format((notDupURL.index(repo)+1), repo), end='')
            NFP.append([repo, err])
            continue # start the loop over and try the next repo.
        # Repo can't be found
        except exceptions.ConnectionError as err:
            print ('\033[K  {0} Packages not Found!!! {1}, 404\r'.format((notDupURL.index(repo)+1), repo), end='')
            NFP.append([repo, err])
            continue # start the loop over and try the next repo.
        # will exit loop instead of killing the script
        except KeyboardInterrupt:
            break

    packagesURL = []
    packagesFiles = []
    packagesEXT = []
    releaseFile = []

    for url in packagesFilesLAC:

        if url[0] in notDupURL:

            rfIndex = notDupURL.index(url[0])

            packagesURL.append(url[0])

            packagesFiles.append(url[1])

            packagesEXT.append(url[2])
            
            releaseFile.append(notDupRelease[rfIndex])

        else:
            continue

    return (packagesURL, packagesFiles, packagesEXT, releaseFile, NFP)