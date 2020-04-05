import json
import timeit
#import plotly.graph_objects as go
import numpy as np

filename= 'memc_1998_entities.jsons'
entity_type= 'person'
data = []

for line in open(filename, 'r'):

    data.append(json.loads(line))



def totalRecords(data):
    print('Total number of records is  ',len(data))


def types(data):
    start = timeit.default_timer()
    uniqueWords = []
    allWords = []

    for i in data:
        for j in i['entities']:
            allWords.append(j['type'])
            if (j['type']) not in uniqueWords:
                uniqueWords.append((j['type']))

    countList = []

    for i in uniqueWords:
        count = allWords.count(i)

        countList.append(i + ' ' + str(count))

    stop = timeit.default_timer()
    print('Time: ', stop - start)
    print(countList)

#types(data)

def nameCount(data, entity_type):
    start = timeit.default_timer()
    uniqueWords = []
    allWords = []

    for i in data:
        for j in i['entities']:
            if (j['type']) == entity_type:
                allWords.append(j['name'])

    for i in allWords:
        if i not in uniqueWords:
            uniqueWords.append(i);


    stop = timeit.default_timer()
    print('Time: ', stop - start)

    # print (len(uniqueWords))


def pop(data):
    start = timeit.default_timer()
    allWords = []

    for i in data:
        for j in i['entities']:
            if (j['type']) == entity_type:
                allWords.append(j['name'])

    uniqueWords = []

    for i in allWords:
        if i not in uniqueWords:
            uniqueWords.append(i);
    countList = []

    for i in uniqueWords:
        count = allWords.count(i)

        countList.append(str(count))

    spreadList = []
    uni = []
    for i in countList:
        spread = countList.count(i)
        if i not in uni:
            uni.append(i)
            spreadList.append({'occurrence of': i, 'count': spread})

    # return (spreadList)
    s = sorted(spreadList, key=lambda i: int(i['occurrence of']), reverse=False)
    # return len(countList)

    occ = []
    cou = []

    for i in s:
        occ.append(i['occurrence of'])
        cou.append(i['count'])

    # fig = go.Figure(data=[go.Table(
    #     header=dict(values=['Word occurances', 'Count'],
    #                 line_color='darkslategray',
    #                 fill_color='grey',
    #                 align='left'),
    #     cells=dict(values=[occ,  # 1st column
    #                        cou],  # 2nd column
    #                line_color='darkslategray',
    #                fill_color='white',
    #                align='left'))
    # ])
    #
    # fig.update_layout(width=500, height=3000)
    # fig.show()
    stop = timeit.default_timer()
    print('Time: ', stop - start)
pop(data)

def spread(data):
    start = timeit.default_timer()
    org_loc_ppl_count = 0
    org_loc_count = 0
    org_ppl = 0
    loc_ppl_count = 0
    org_count = 0
    ppl_count = 0
    loc_count = 0

    for i in data:
        org = False
        loc = False
        ppl = False

        for j in i['entities']:

            if j['type'] == 'organization':
                org = True

            elif j['type'] == 'location':
                loc = True

            elif j['type'] == 'person':
                ppl = True

        if org and loc and ppl:
            org_loc_ppl_count = org_loc_ppl_count + 1

        elif org and loc and ppl == False:
            org_loc_count = org_loc_count + 1

        elif org and loc == False and ppl:
            org_ppl = org_ppl + 1

        elif org == False and loc and ppl:
            loc_ppl_count = loc_ppl_count + 1

        elif org and loc == False and ppl == False:
            org_count = org_count + 1

        elif org == False and loc and ppl == False:
            loc_count = loc_count + 1

        elif org == False and loc == False and ppl:
            ppl_count = ppl_count + 1
    #
    # print( ' Organisation and location and person:   ' + str(org_loc_ppl_count ), \
    #        '\n Organisation and location: ' + str(org_loc_count), \
    #        '\n Organisation and person: ' + str(org_ppl), \
    #        '\n Location and person: ' + str(loc_ppl_count), \
    #        '\n Organisation: ' + str(org_count), \
    #        '\n Location: ' + str(loc_count), \
    #        '\n Person: ' + str(ppl_count))
    stop = timeit.default_timer()
    print('Time: ', stop - start)


# totalRecords(data)
# types(data)
# nameCount(data, entity_type)
# spread(data)
#pop(data)