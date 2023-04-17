import json

dico = dict()
with open('test/1.reseau', 'r') as file:
    header = file.readline()
    nodes = header.replace('"', '').replace('\n', '').split(',')
    for l_i, line in enumerate(file):
        print(line)
        for c_i, value in enumerate(line.split(',')):
            print(value)
            if int(value) == 1:
                node_name = str(nodes[l_i]) + "-" + str(nodes[c_i])
                dico[node_name] = {'length': 100}

json_ = json.dumps(dico)
with open("2.aretesf", "w") as f:
    f.write(json_)