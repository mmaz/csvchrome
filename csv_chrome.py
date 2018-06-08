import subprocess
import csv

get_template = """osascript -e 'set text item delimiters to linefeed' -e 'tell app "google chrome" to {} of tabs of window {} as text'"""

def getUrls(windowId : int) -> str:
    return get_template.format("url", windowId)
def getTitles(windowId : int) -> str:
    return get_template.format("title", windowId)

def getWindow(windowId : int) -> [(str,str)]:
    getproc = lambda s : subprocess.run(s, shell=True, check=True, stdout=subprocess.PIPE)
    urlp   = getproc(getUrls(windowId))
    titlep = getproc(getTitles(windowId))
    urls   = urlp.stdout.decode("utf-8").splitlines()
    titles = titlep.stdout.decode("utf-8").splitlines()
    return list(zip(titles,urls))

def getAllWindows(maxWindow : int) -> [(str,str)]:
    """maxWindow is 1-indexed"""
    allWindows = []
    for widx in range(1, maxWindow + 1):
        ws = getWindow(widx)
        allWindows.extend(ws)
    return allWindows

def windows2csv(fn, windows):
    with open(fn, 'w',) as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(windows)
