from requests import get, exceptions

def getRepoFile(repoURL):
    
    repoFile = get(repoURL, headers={"User-Agent":"Debian APT-HTTP/1.3 (2.1.10)"}, timeout=2)
    
    return (repoFile, repoFile.status_code)
    