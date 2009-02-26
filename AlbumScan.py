import os
import stat
import config

def treeEntryToAlbum(path, trackGrouping):
    '''Given a directory tree entry, semantically deduce whether
    it is an album. 
    Two cases are considered:
    Artist - Album 
    Artist / Album
    ''' 
    dirDepth = len(path.split(os.sep)) - len(config.rootDir.split(os.sep))
    dirs = path.split(os.sep)[0-dirDepth:]
    print "%r deep, %r entries\n%s\n-------" % (dirDepth, len(trackGrouping), path)

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

for key, val in trackGroupings.items():
    treeEntryToAlbum(key, val)
