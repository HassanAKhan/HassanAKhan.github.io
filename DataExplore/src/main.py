from elasticsearch import Elasticsearch
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import plotly.graph_objects as go


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


app = Flask(__name__)
api = Api(app)
CORS(app)

year = '1998'
entity_type = 'person'

class EntityList(Resource):

    def get(self):

        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            },
        }
        res = es.search(index=year, body=doc, scroll='1m')

        resource = []
        for doc in res['hits']['hits']:
            d=doc['_source']['entities']

            resource.append(d)

        return resource


api.add_resource(EntityList, '/alldata')

class EntityListTypes(Resource):

    def get(self):

        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            },
        }
        res = es.search(index=year, body=doc, scroll='1m')

        resource = []
        for doc in res['hits']['hits']:
            d=doc['_source']['entities']

            resource.append(d)
        allWords = []

        for i in range(len(resource)):
                for j in range(len(resource[i])):
                    allWords.append(resource[i][j]['type'])
        uniqueWords = []

        for i in allWords:
            if i not in uniqueWords:
                uniqueWords.append(i);
        countList = []
        for i in uniqueWords:
            count = allWords.count(i)

            countList.append(i +' ' + str(count))

        return countList


api.add_resource(EntityListTypes, '/types')


class EntityListName(Resource):

    def get(self):

        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            },
        }
        res = es.search(index=year, body=doc, scroll='1m')

        resource = []
        for doc in res['hits']['hits']:
            d=doc['_source']['entities']

            resource.append(d)
        allWords = []

        for i in range(len(resource)):
                for j in range(len(resource[i])):
                    if resource[i][j]['type'] == entity_type:
                        allWords.append(resource[i][j]['name'])
        uniqueWords = []

        for i in allWords:
            if i not in uniqueWords:
                uniqueWords.append(i);
        countList = []
        for i in uniqueWords:
            count = allWords.count(i)

            countList.append({'type': entity_type, 'name': i, 'count': count})

        return sorted(countList, key = lambda i: i['count'], reverse=True)
        #return len(countList)


api.add_resource(EntityListName, '/names')


class EntityListNameSpread(Resource):

    def get(self):

        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            },
        }
        res = es.search(index=year, body=doc, scroll='1m')

        resource = []
        for doc in res['hits']['hits']:
            d=doc['_source']['entities']

            resource.append(d)
        allWords = []

        for i in range(len(resource)):
                for j in range(len(resource[i])):
                    if resource[i][j]['type'] == entity_type:
                        allWords.append(resource[i][j]['name'])
        uniqueWords = []

        for i in allWords:
            if i not in uniqueWords:
                uniqueWords.append(i);
        countList = []

        for i in uniqueWords:
            count = allWords.count(i)

            countList.append(str(count))

        spreadList = []
        uni= []
        for i in countList:
            spread = countList.count(i)
            if i not in uni:
                uni.append(i)
                spreadList.append({'occurrence of': i, 'count': spread})

        #return (spreadList)
        s= sorted(spreadList, key = lambda i: int(i['occurrence of']),reverse=False)
        #return len(countList)

        occ= []
        cou= []

        for i in s :
            occ.append(i['occurrence of'])
            cou.append(i['count'])

        fig = go.Figure(data=[go.Table(
            header=dict(values=['Word occurances', 'Count'],
                        line_color='darkslategray',
                        fill_color='grey',
                        align='left'),
            cells=dict(values=[occ,  # 1st column
                               cou],  # 2nd column
                       line_color='darkslategray',
                       fill_color='white',
                       align='left'))
        ])

        fig.update_layout(width=500, height=3000)
        fig.show()


api.add_resource(EntityListNameSpread, '/names_spread')

class EntityListNamePop(Resource):

    def get(self):

        doc = {
            'size': 10000,
            'query': {
                'match_all': {}
            },
        }
        res = es.search(index=year, body=doc, scroll='1m')

        resource = []
        for doc in res['hits']['hits']:
            d=doc['_source']['entities']
            resource.append(d)

        org_loc_ppl_count = 0
        org_loc_count = 0
        org_ppl = 0
        loc_ppl_count = 0
        org_count= 0
        ppl_count= 0
        loc_count= 0

        for i in resource:
            org = False
            loc = False
            ppl = False

            for j in i:
                if j['type'] == 'organization':
                    org= True

                elif j['type'] == 'location':
                    loc= True

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



        return 'Organisation and location and person:   ' + str(org_loc_ppl_count),\
               'Organisation and location: ' + str(org_loc_count),\
               'Organisation and person: ' + str(org_ppl),\
               'Location and person: ' + str(loc_ppl_count),\
               'Organisation: ' + str(org_count),\
               'Location: ' + str(loc_count),\
               'Person: ' + str(ppl_count)

        #return resource
        #return len(resource)

api.add_resource(EntityListNamePop, '/names_pop')

class EntityListTest(Resource):

    def get(self):

        doc = {
            "query": {
                "term": {
                    'resource.id': "1996-C5432410-28911_551_9"
                }
            },
        }
        res = es.search(index=year, body=doc, scroll='1m')

        return res


api.add_resource(EntityListTest, '/specific')


