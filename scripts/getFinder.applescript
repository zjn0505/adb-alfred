tell application "Finder"
	try
        set pathList to POSIX path of (folder of the front window as alias)
    on error
        set pathList to POSIX path of (path to desktop folder as alias)
    end try
	
	return pathList
end tell
