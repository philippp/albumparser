import os
import stat
import config
import re


def decodeDirName(path, trackGrouping):
    '''Given a directory tree entry, semantically deduce whether
    it is an album. 
    Two cases are considered:
    Artist - Album 
    Artist / Album
    ''' 
    dirNamesClean, dirNamesSort = [], []
    dirDepth = len(path.split(os.sep)) - len(config.rootDir.split(os.sep))
    dirs = path.split(os.sep)[0-dirDepth:]
    
    for idx, dirName in enumerate(dirs):
       dirNameClean, dirNameSort = nameToParts( dirName )
       dirNamesClean.append( dirNameClean )
       dirNamesSort.append( dirNameSort )
    if len(dirNamesSort) == 1 or cmp(dirNamesSort[0], dirNamesSort[1]) == 0:
        artist, album = cleanNameParse( dirNamesClean[0] )
    else:
        artist = dirNamesClean[0]
        album = dirNamesClean[1]

    return artist, album


def cleanNameParse( cleanName ):
    '''Attempt to infer the artist and album from a single directory name.'''
    nameParts = cleanName.split("-")
    if len( nameParts ) == 1:
        artistName = albumName = cleanName
    else:
        artistName = "-".join(nameParts[0:-1])
        albumName = nameParts[-1:][0]
    return artistName, albumName

def nameToParts( dirName ):
    ''' Filters unused information from a directory name and splits each name by -
    returns (cleanNameParts, sortNameParts)'''
    blackList = '' #regex of ignored labeling, See config.dirNameBlacklist in config.py
    for listItem in config.dirNameBlacklist:
        blackList += '(%s)*' % listItem
    cleanName = re.sub(blackList,'',dirName)
    sortName = "".join(re.findall('([\d\w\-]+)',cleanName)).lower()    
    return cleanName, sortName



def scanTree(path):
    '''Recursively scan a directory tree and find groups of albums'''
    trackGroupings = {} ## indexed by path
    for entry in os.listdir( path ):
        entryPath = path+os.sep+entry
        entryStat = os.stat(entryPath)
        if stat.S_ISDIR( entryStat[0] ):
            trackGroupings.update( scanTree( entryPath ) )
        elif entry.split(os.extsep)[-1] in config.audioExtensions:
            parentEntryPath = os.sep.join(entryPath.split(os.sep)[0:-1])
            trackGroupings[parentEntryPath] = trackGroupings.get(parentEntryPath,None) or []
            trackGroupings[parentEntryPath].append((entryPath, entry))
    return trackGroupings


trackGroupings = scanTree( config.rootDir )

for dirName, trackGrouping in trackGroupings.items():
    artist, album = decodeDirName(dirName, trackGrouping)
    print "Artist: %s\nAlbum: %s" % (artist, album)
    print "%r entries\n%s\n-------" % (len(trackGrouping), dirName)     
