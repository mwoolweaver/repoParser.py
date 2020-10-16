from datetime import datetime
from time import sleep

from lib.getLists import getLists
from lib.getRelease import findDUPrelease
from lib.getPackages import getPackages
from lib.getCydiaIcon import getCydiaIcon, get

import os
import glob

Pfiles = glob.glob(r'Packages/*.Packages')
Rfiles = glob.glob(r'Release/*')
CIfiles = glob.glob(r'CydiaIcon/*')


for a in Pfiles:
    try:
        os.unlink(a)
    except OSError as e:
        print("Error: %s : %s" % (a, e.strerror))
for b in Rfiles:
    try:
        os.unlink(b)
    except OSError as e:
        print("Error: %s : %s" % (b, e.strerror))
for c in CIfiles:
    try:
        os.unlink(c)
    except OSError as e:
        print("Error: %s : %s" % (c, e.strerror))

print ("Deleted old data.")
startTime = datetime.now()

# Where we source our repo list from
print("\033c")

repoList = getLists()

listBeforeCheck = repoList[0]    # The list of repos we continue using
listBeforeCheckDUP = repoList[1] # nuber of duplicate URL's
WithIssuesInLBC = repoList[2]    # number repos we found that we know cause issues
defaultInLBC = repoList[3]       # number of default repo we found that we don't need since the come with our package manager

print ("Found and Removed " + str(len(listBeforeCheckDUP)) + " duplicate repo URL's.")
print (" ")
print ("Found " + str(len(defaultInLBC)) + " default repos that will not be add to list.")
print (" ")
print ("Found " + str(len(WithIssuesInLBC)) + " repos that could cause issues that weren't add to list.")
print (" ")
print ("Checking the " + str(len(listBeforeCheck)) + " unique repos on Parcility & iOS Repo Updates combined.")
print (" ")

# sort the list alphabetically just so there is some predictability
listBeforeCheck.sort()
# check for Release for each repo
listRelease = findDUPrelease(listBeforeCheck)

notDupRelease = listRelease[0]
notDupURL = listRelease[1]

isDupURL = listRelease[2]
isDupRelease = listRelease[3]
notValidRelease = listRelease[4]
noFindRelease = listRelease[5]
oldAS = listRelease[6]
oldGH = listRelease[7]
oldGL = listRelease[8]
oldHTTP = listRelease[9]
notChanged = listRelease[10]

print (" ")
print (" ")
print ("Could not find " + str(len(noFindRelease)) + " Release file(s).")
print (" ")
print ("Found " + str(len(notValidRelease)) + " repo(s) with NOT valid release file(s)")
print (" ")
print ("Found " + str(len(isDupRelease)) + " repos with duplicate release files.")
print (" ")
print ("Found " + str(len(oldGH)) + " old github URL's that were changed to custom url.")
print (" ")
print ("Found " + str(len(oldGL)) + " old gitlab URL's that were changed to custom url.")
print (" ")
print ("Found " + str(len(oldAS)) + " old appspot URL's that were changed to custom url.")
print (" ")
print ("Found " + str(len(oldHTTP)) + " old http URL's changed to https.")
print (" ")
print ("Found " + str(len(notChanged)) + " URL's that didn't change even tho the release file was the same.")
print (" ")
print ("Found " + str(len(notDupURL)) + " valid repos to be added to list.")
print (" ")
print ("Checking "+ str(len(notDupURL)) + " repos for Packages file")
print (" ")
print (" ")

# check for Packages.(zst|xz|lzma|bz2|gz) for each repo
listPackages = getPackages(notDupURL, notDupRelease)

packagesURL = listPackages[0]   # repo URL's
packagesFiles = listPackages[1] # repo Packages files
packagesEXT = listPackages[2]   # Packages file compression type
releaseFile = listPackages[3]   # repo release file
noFindPackages = listPackages[4]

print (" ")
print (" ")
print ("Failed to find " + str(len(noFindPackages)) + " Packages.(zst|xz|lzma|bz2|gz) files.")
print (" ")
print ("Found " + str(len(packagesURL)) + " Packages.(zst|xz|lzma|bz2|gz) files.")
print (" ")
print (" ")

# CydiaIcon.png for each repo
cydiaIcons = getCydiaIcon(packagesURL)

iconsPNG = cydiaIcons[0]
noCydiaIcon = cydiaIcons[1]

print (" ")
print (" ")
print ("Failed to find " + str(len(noCydiaIcon)) + " Cydia Icons.")
print (" ")
print ("Found " + str(len(iconsPNG)) + " Cydia Icons.")
print (" ")


# create file with validated repo list
with open('just-urls.list', 'w') as f:
    for url in packagesURL:
        if url != None:
            f.write("%s\n" % url)
        else:
            continue

print (" ")
print ("Successfully wrote " + str(len(packagesURL)) + " URL's to just-urls.list.")
print (" ")

with open('sources.list', 'w') as f:
    for url in packagesURL:
        if url != None:
            f.write("deb %s/ ./\n" % url)
        else:
            continue

print (" ")
print ("Successfully wrote " + str(len(packagesURL)) + " sources to sources.list.")
print (" ")

# save Release files
for release in releaseFile:
    if release != None:
        
        indexPURL = releaseFile.index(release)
        fileToSaveTo = "Release/" + str(indexPURL) + ".Release"
        dataToSave = release

        with open(fileToSaveTo, 'wb') as f:
            f.write(dataToSave)
  
    else:
        continue

print (" ")
print ("Successfully wrote " + str(len(packagesURL)) + " Release files.")
print (" ")

# save Packages file (should be indexed the same as Release Files)
for packages in packagesFiles:
    if packages != None:
        indexPURL = packagesFiles.index(packages)
        fileToSaveTo = "Packages/" + str(indexPURL) + ".Packages"
        dataToSave = packages
        with open(fileToSaveTo, 'wb') as f:
            f.write(dataToSave)

    else:
        continue

print (" ")
print ("Successfully wrote " + str(len(packagesURL)) + " Packages files.")
print (" ")


print (" ")
print ("Successfully wrote " + str(len(iconsPNG)) + " Cydia Icons.")
print (" ")

print (" ")
print (" ")
print ("Time Started")
print (startTime)
print ("Time to complete")
print (datetime.now() - startTime)
print ("Time Completed")
print (datetime.now())