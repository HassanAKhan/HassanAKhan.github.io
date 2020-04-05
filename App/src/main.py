from flask import  Flask, render_template, jsonify, request, make_response
import json
from pymnet import *
import easygui as es
from datetime import datetime
import dateutil.parser





app = Flask(__name__)
app.debug = True
app.config["DEBUG"] = True
files = []
file_data = []
new_data =[]
TEMPLATES_AUTO_RELOAD = True



#Main function to get and send requested data
@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        data = json.loads(request.data)
        print (data)
        if data == 'selectFile':
            filename = es.fileopenbox()
            files.append(filename)

            for line in open(filename, 'r'):
                file_data.append(json.loads(line))


        elif data == 'render':
            render_data = render(file_data)
            return make_response(jsonify(render_data), 201)

        elif data[0] == 'date':
            if data[1] == '':
                render_data = render(file_data)
                return make_response(jsonify(render_data), 201)

            new_data = filterFunction(data,files[0])
            render_data = filterRender(new_data)
            return make_response(jsonify(render_data), 201)

        elif data[0] == 'search':
            if data[1] == '':
                render_data = render(file_data)
                return make_response(jsonify(render_data), 201)

            new_data = searchFilter(data,files[0])
            render_data = render(new_data)
            return make_response(jsonify(render_data), 201)


    return render_template('index.html',
                           entity_types=types(file_data),
                           total_records=totalRecords(file_data),
                           occ_count=types_count(file_data),
                           pop=pop(file_data, totalRecords(file_data)),
                           render_data=render(file_data)
                           )

#Returns the total number of records in the data file
def totalRecords(data):
    print('Total number of records is  ', len(data))
    return(len(data))

#Checks how many entities are present and returns them
def types(data):

    uniqueWords = []
    allWords = []
    for i in data:
        for j in i['entities']:
            allWords.append(j['type'])
            if (j['type']) not in uniqueWords:
                uniqueWords.append((j['type']))
    return(uniqueWords)

#Returns a non-unique count of the entities
def types_count(data):

    uniqueWords = []
    allWords = []

    for i in data:
        for j in i['entities']:
            allWords.append(j['type'])
            if (j['type']) not in uniqueWords:
                uniqueWords.append((j['type']))

    countList = {}

    for i in uniqueWords:
        count = allWords.count(i)

        countList[i] = str(count)

    return(countList)

def pop(data, total):

    org_loc_ppl_count = 0
    org_loc_count = 0
    org_ppl = 0
    loc_ppl_count = 0
    org_count = 0
    ppl_count = 0
    loc_count = 0

    if total == 0 :
        population = [{'OLP': org_loc_ppl_count, 'percentage': 0},
                      {'OL': org_loc_count, 'percentage': 0},
                      {'OP': org_ppl, 'percentage': 0},
                      {'LP': loc_ppl_count, 'percentage': 0},
                      {'O': org_count, 'percentage': 0},
                      {'L': loc_count, 'percentage': 0},
                      {'P': ppl_count, 'percentage': 0}
                      ]
        return population


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

    population = [{'OLP': org_loc_ppl_count, 'percentage':str(round(((org_loc_ppl_count / total) * 100), 2))+'%'},
                  {'OL': org_loc_count, 'percentage': str(round(((org_loc_count / total) * 100), 2))+'%'},
                  {'OP': org_ppl, 'percentage': str(round(((org_ppl / total) * 100), 2))+'%'},
                  {'LP': loc_ppl_count, 'percentage': str(round(((loc_ppl_count / total) * 100), 2))+'%'},
                  {'O': org_count, 'percentage': str(round(((org_count / total) * 100), 2))+'%'},
                  {'L': loc_count, 'percentage': str(round(((loc_count / total) * 100), 2))+'%'},
                  {'P': ppl_count, 'percentage': str(round(((ppl_count / total) * 100), 2))+'%'}
                  ]

    return (population)

def  render(data):

    data= data[0:1]
    print(data)
    nodes = []
    struct = []
    mnet = MultilayerNetwork(aspects= 1, fullyInterconnected=False)
    for i in data:

        d=i['entities']

        # for i in range(len(d)):
        #     if d[i]['type']== 'person':
        #         nodes.append(d[i])
        for i in range(len(d)):
            nodes.append(d[i])
            #print(d[i])



        for i in range(len(nodes)):
            if len(nodes) > 1:
                i=0
                first_node_name = nodes[i]['name']
                first_node_layer = nodes[i]['type']

                nodes.pop(i)
                for j in range(len(nodes)):

                    second_node_name = nodes[j]['name']
                    second_node_layer = nodes[j]['type']
                    struct.append([first_node_name, second_node_name, first_node_layer, second_node_layer])

    #print(data[0]['entities'])
    for i in struct:
        mnet[i[0],i[1],i[2],i[3]] =1


    return( webplot(mnet,struct ,outputfile=None, mult_layer=True))

def filterFunction(data, filename):
    start = (datetime.strptime(data[1], '%Y-%m-%d'))
    end = (datetime.strptime(data[2], '%Y-%m-%d'))
    file_data = []
    for line in open(filename, 'r'):
        loaded = json.loads(line)
        in_date = dateutil.parser.parse(loaded['resource']['lodging_date'])
        in_date = in_date.strftime('%Y-%m-%d')
        in_date = datetime.strptime(in_date, '%Y-%m-%d')

        if start <= in_date <= end:
            file_data.append(loaded)
        else:
            continue
    return file_data

def searchFilter (data , filename):
    file_data = []
    for line in open(filename, 'r'):
        loaded = json.loads(line)

        if loaded['resource']['id'] == data :
            file_data.append(loaded)
            return file_data
        else:
            continue
    return ('not found')

def  filterRender(data):
    data = data[0:10]
    nodes = []
    struct = []
    mnet = MultilayerNetwork(aspects= 1, fullyInterconnected=False)
    for i in data:

        d=i['entities']

        # for i in range(len(d)):
        #     if d[i]['type']== 'person':
        #         nodes.append(d[i])
        for i in range(len(d)):
            nodes.append(d[i])
            #print(d[i])



        for i in range(len(nodes)):
            if len(nodes) > 1:
                i=0
                first_node_name = nodes[i]['name']
                first_node_layer = nodes[i]['type']

                nodes.pop(i)
                for j in range(len(nodes)):

                    second_node_name = nodes[j]['name']
                    second_node_layer = nodes[j]['type']
                    struct.append([first_node_name, second_node_name, first_node_layer, second_node_layer])

    #print(data[0]['entities'])
    for i in struct:
        mnet[i[0],i[1],i[2],i[3]] =1


    return( webplot(mnet,struct ,outputfile=None, mult_layer=True))


def pythonImplemntation(data):

    nodes = []
    struct = []
    mnet = MultilayerNetwork(aspects= 1, fullyInterconnected=False)
    for i in data:

        d=i['entities']

        # for i in range(len(d)):
        #     if d[i]['type']== 'person':
        #         nodes.append(d[i])
        for i in range(len(d)):
            nodes.append(d[i])
            #print(d[i])



        for i in range(len(nodes)):
            if len(nodes) > 1:
                i=0
                first_node_name = nodes[i]['name']
                first_node_layer = nodes[i]['type']

                nodes.pop(i)
                for j in range(len(nodes)):

                    second_node_name = nodes[j]['name']
                    second_node_layer = nodes[j]['type']
                    struct.append([first_node_name, second_node_name, first_node_layer, second_node_layer])








    #print(data[0]['entities'])
    for i in struct:
        mnet[i[0],i[1],i[2],i[3]] =1


    fig = draw(mnet, show=True, layout= 'spring')

    #fig = draw(er(50,3*[0.9]), show=True)
    #print( webplot(mnet,struct ,outputfile=None, mult_layer=True))




