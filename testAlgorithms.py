#funzione ricorsiva che dati un esempio del dataset e un nodo dell'albero di decisione prosegue la ricerca della
#classificazione dell'esempio finche' non giunge ad un nodo foglia
def testRow(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['leftChild'],dict):
            return testRow(node['leftChild'], row)
        else:
            return node['leftChild']
    else:
        if isinstance(node['rightChild'],dict):
            return testRow(node['rightChild'], row)
        else:
            return node['rightChild']


#funzione che prende in ingresso le classificazioni note e ricavate di un insieme di esempi test e le confronta
#stabilendo la percentuale di accuratezza dell'albero di decisione utilizzato
def accuracy(known, learned):
    percentage = 0
    for i in range(len(known)):
        if known[i] == learned[i]:
            percentage = percentage + 1
    return percentage / float(len(known)) * 100


#funzione che dato un insieme di esempi lo splitta secondo la logica di una 10-fold-cross-validation stratificata
def stratified10FoldCrossValidationSplit(examples):
    tmp = list(examples)
    classes = list(set([row[-1] for row in examples]))
    groups = []
    #prima si divide gli esempi in gruppi in base alla loro classificazione, poi si procede prelevando il 10% degli
    #elementi di ogni gruppo per formare un fold
    for c in classes:
        group = []
        for i in range(len(tmp)):
            if tmp[i][-1] == c:
                group.append(tmp[i])
        groups.append(group)
    folds = []
    groupsSize = [int(len(group)/10) for group in groups]
    for i in range(10):
        fold = []
        for j in range(len(groups)):
            for k in range(groupsSize[j]):
                fold.append(groups[j].pop(0))
        folds.append(fold)
    #in questa parte gli esempi avanzati in ogni gruppo di classificazione (a causa dell'approssimazione a intero della
    #divisione per 10) sono ridistribuiti nei vari fold
    for g in groups:
        cont = 0
        while len(g) > 0:
            folds[cont].append(g.pop(0))
            cont = cont +1
    return folds