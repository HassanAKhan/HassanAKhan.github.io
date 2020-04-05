import math,json,os
from .net import MultilayerNetwork

def write_mult(net, struct):
    """Writes a multiplex network with a single aspect in a JSON format.
    """
    assert isinstance(net,MultilayerNetwork)
    assert net.aspects==0 or net.aspects==1
    nets={}
    node2index={}
    nets["nodes"]=[]

    # for i,node in enumerate(net):
    #
    #     nets["nodes"].append({"name":node})
    #     node2index[node]=i
    # for layer in net.get_layers():
    #
    #     for elm in net.iter_nodes(layer):

    for i,elm in enumerate(net.iter_node_layers()):
        nets["nodes"].append({"name": elm[0], "layer":elm[1]})
        node2index[elm[0]] = i


    #print(net.iter_node_layers())

    layer2index={}
    nets["layers"]=[]
    for i,layer in enumerate(net.get_layers()):
        nets["layers"].append({"name":layer})
        layer2index[layer]=i

    nets["links"]=[]

    for i in nets["nodes"]:
        i['layer']=(layer2index[i['layer']])


    # print(struct)
    #
    # print(json.dumps(nets))

    for elm in struct:
        nets["links"].append({"source":node2index[elm[0]],
                                "target":node2index[elm[1]],
                                "value" :1,
                                "layer" :layer2index[elm[2]],
                                "layer_to":layer2index[elm[3]]})



    # for layer in net.get_layers():
    #     for edge in net.A[layer].edges:
    #         print(edge)
    #
    #         nets["links"].append({"source":node2index[edge[0]],
    #                               "target":node2index[edge[1]],
    #                               "value" :edge[2],
    #                               "layer" :layer2index[layer]})

    print(json.dumps(nets))
    return json.dumps(nets)

