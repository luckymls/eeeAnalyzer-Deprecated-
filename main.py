# Author: Melis Luca <melis.luca2014@gmail.com>
# License: BSD 3 clause

from math import ceil
import re
import urllib.request
import time

def regOnce(pattern, data, num):

    matches = re.findall(pattern,data)
    return matches[0][num:]
     

base_url = 'http://90.147.170.141/monitor/dqmreport2/'
end_url = '/?C=M;O=D'

print('Author: Melis Luca','License: BSD 3 clause')

# GET Telescope List

print('Ottengo nomi telescopi...')

reqList = str(urllib.request.urlopen('http://90.147.170.141/monitor/').read())

patternList_1 = r'class="bold bigtab">\w{4}-\d{2}'
matchesList = re.findall(patternList_1, reqList)

telescope_list = []
telescope_data = {}
for telescope in matchesList:
    telescope = telescope[20:].upper()
    telescope_list.append(telescope)
    telescope_data[telescope] = {}
    telescope_data[telescope]['data'] = {} # TORI-02': {'data': {} }

    
# GET Each Telescope List {date - file}

print('Ottengo date eventi...')

patternDate_1 = r'href="\d{4}-\d{2}-\d{2}'
dateNumber = 0
for telescope in telescope_list:
    
    url = base_url+telescope+end_url
    reqFirst = str(urllib.request.urlopen(url).read())
    matchesFirst = re.findall(patternDate_1, reqFirst)

    for match in matchesFirst:
        match = match[6:]
        dateNumber += 1
        telescope_data[telescope]['data'][match] = {}

     
# GET Events Number

print('Ottengo informazioni eventi... (Questa operazione richiede alcuni minuti)')

patternNumberEvent = r'Total number of events: \d+'
dateChecked=0 


for telescope in telescope_data:

    for data in telescope_data[telescope]['data']:

        perc = round((dateChecked*100)/dateNumber,2)
        urlData = f'http://90.147.170.141/monitor/dqmreport2/{telescope}/{data}'
        dataReq = str(urllib.request.urlopen(urlData).read())
        dateChecked += 1
        #Run Processed
        result = regOnce(r'Number of runs processed: \d+', dataReq, 26)
        telescope_data[telescope]['data'][data]['runsProcessed'] = result
        
        # Total Events
        result = regOnce(r'Total number of events: \d+', dataReq, 24)
        telescope_data[telescope]['data'][data]['totalEvent'] = result

        # Events with hits
        result = regOnce(r'Number of runs processed: \d+',dataReq, 26)
        telescope_data[telescope]['data'][data]['eventsWithHits'] = result

        # Events with tracks
        result = regOnce(r'Number of events with a track: \d+',dataReq, 31)
        telescope_data[telescope]['data'][data]['eventsWithTracks'] = result
        
    print(f'\r{perc}%')
    
print('Pronto.')



while True:
    try:
        telescope = str(input('Inserire nome telescopio per ottenere informazioni:\n'))
        if len(telescope_data[telescope.upper()]['data']) is 0:
           res = 'Telescopio non in funzione.'
        else:
           res = telescope_data[telescope.upper()]
        print(res)
    

    except:
        print('Telescopio non trovato, riprovare \n')
