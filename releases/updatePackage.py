#!/usr/bin/python
import json, sys, copy, hashlib, os

archiveBaseURL =  "https://raw.githubusercontent.com/modulolabs/arduino-hardware/master/releases/"
indexFile = 'package_modulo_index.json'
# Gather some info about the package
version = sys.argv[1]
archiveFile = 'package_modulo_%s.zip' % version
hash = hashlib.sha256()
hash.update(open(archiveFile).read())
fileSize = os.stat(archiveFile).st_size

# Load the package index file
data = json.load(open(indexFile,'r'))

# Find the platform dict within the package index file
currentPlatform = None
for platform in data['packages'][0]['platforms'] :
    # If we find the exact version, use it
    if (platform['version'] == version) :
        currentPlatform = platform
        break

    # Find the most recent version
    if (currentPlatform is None or float(platform['version']) > float(currentPlatform['version'])) :
        currentPlatform = platform

# If we didn't find the exact version, make a copy
if currentPlatform['version'] != version :
    currentPlatform = copy.deepcopy(currentPlatform)
    currentPlatform['version'] = version
    data['packages'][0]['platforms'].append(currentPlatform)


# Store the new data bout the platform
currentPlatform['archiveFileName'] = archiveFile
currentPlatform['checksum'] = 'SHA-256:' + hash.hexdigest()
currentPlatform['size'] = str(fileSize)
currentPlatform['url'] = archiveBaseURL + archiveFile

# Save the file
json.dump(data, open(indexFile, 'w'), indent=4)
