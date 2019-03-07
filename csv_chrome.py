import subprocess
import datetime
import csv

get_template = """osascript -e 'set text item delimiters to linefeed' -e 'tell app "google chrome" to {} of tabs of window {} as text'"""

def getUrls(windowId : int) -> str:
    return get_template.format("url", windowId)
def getTitles(windowId : int) -> str:
    return get_template.format("title", windowId)

def getWindow(windowId : int) -> [(str,str)]:
    getproc = lambda s : subprocess.run(s, shell=True, check=True, stdout=subprocess.PIPE)
    urlp    = getproc(getUrls(windowId))
    titlep  = getproc(getTitles(windowId))
    urls    = urlp.stdout.decode("utf-8").splitlines()
    titles  = titlep.stdout.decode("utf-8").splitlines()
    titles_urls = zip(titles,urls)
    return list(map(lambda tu: [windowId] + list(tu), titles_urls))

def getAllWindows(maxWindow : int) -> [(str,str)]:
    """maxWindow is 1-indexed"""
    allWindows = []
    for widx in range(1, maxWindow + 1):
        ws = getWindow(widx)
        allWindows.extend(ws)
    return allWindows

def windows2csv(fn, windows):
    with open(fn, 'w',) as fh:
        writer = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(windows)

def countWindows() -> int:
    chromeWindows = """osascript -e 'tell app "google chrome" to count of windows as text'"""
    countp = subprocess.run(chromeWindows, shell=True, check=True, stdout=subprocess.PIPE)
    counts = countp.stdout.decode("utf-8").strip()
    return int(counts)

def savetabs(): 
    num_windows = countWindows() #1-indexed
    windows = getAllWindows(num_windows)
    fn = "alltabs_{}.csv".format(datetime.datetime.now().date())
    windows2csv(fn, windows)

if __name__ == "__main__":
    savetabs()
