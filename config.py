rootDir = '/Volumes/G-Drive Q/incoming'
audioExtensions = ['mp3', 'flac', 'm4a', 'mp4', 'mpg2', 'wav', 'wma']
dirNameBlacklist = [
    '(\[.*\])*',          #square brackets [2008]
    '\([vV\dflac]*\)',    #(v0) (flac) etc
    '320',
    'PULSE',
    '[Vv]0']
