import math

def printTree(node, depth=0):
	if isinstance(node, dict):
		print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
		printTree(node['leftChild'], depth+1)
		printTree(node['rightChild'], depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))

#funzione che crea l'albero di decisione splittando il dataset di esempi iniziale per originare la radice e dare il via
#alla ramificazione
def decisionTreeLearning(examples):
    attributesIndex = []
    for k in range(0, len(examples[0]) - 1):
        attributesIndex.append(k)
    root = bestSplit(examples, attributesIndex)
    splitting(root)
    return root


#funzione ricorsiva che splitta il dataset di esempi corispondente ad un nodo dell'albero dando cosi' inizio alla
#ramificazione. Si occupa inoltre di gestire i casi in cui e' necessario arrestarsi originando un nodo foglia
def splitting(node):
    sup, inf = node['sets']
    del (node['sets'])
    # caso 1: lo split produce un ramo senza esempi rimanenti
    # CONSEGUENZA: i due rami generati poratno entrambi ad una stessa foglia contenente la classificazione piu' ricorrente
    #             negli esempi del ramo non vuoto
    if not sup or not inf:
        node['leftChild'] = node['rightChild'] = terminal(sup + inf)
        return
    #caso2: gli attributi del dataset sono gia' stati tutti utilizzati per effettuare uno split
    #CONSEGUENZA: i due rami di questo nodo diventano foglie
    if len(node['attributesIndex']) == 0:
        node['leftChild'] = terminal(inf)
        node['rightChild'] = terminal(sup)
        return
    #caso3: tutti gli esempi di un ramo appartengo alla stessa classificazione
    #CONSEGUENZA: non e' piu' necessario splittare ulteriormente quel ramo percio' esso portera' ad un nodo foglia.
    #             In caso contrario si procede con il normale splitting.
    if sameClassifcation(inf):
        node['leftChild'] = terminal(inf)
    else:
        node['leftChild'] = bestSplit(inf, list(node['attributesIndex']))
        splitting(node['leftChild'])
    if sameClassifcation(sup):
        node['rightChild'] = terminal(sup)
    else:
        node['rightChild'] = bestSplit(sup, list(node['attributesIndex']))
        splitting(node['rightChild'])


#funzione che dato un insieme di esempi testa tutti i possibili split points (ovvero tutti i valori presenti di tutti
#gli attributi validi) restituendo indice, valore e gruppi derivati di quello con information gain maggiore, sotto forma
#di nodo dell'albero di decisione
def bestSplit(examples, attributesIndex):
    print 'Decido il miglior split da fare!'
    examplesClasses = list(set(row[-1] for row in examples))
    attributeIndex = -1
    attributeValue = None
    bestGain = -1
    for i in attributesIndex:
        for j in examples:
            gain = calculateInformationGain(split(examples, i, j[i]), examplesClasses)
            if gain > bestGain:
                attributeIndex = i
                attributeValue = j[i]
                bestGain = gain
    sets = split(examples, attributeIndex, attributeValue)
    attributesIndex.remove(attributeIndex)
    node = {'index':attributeIndex, 'value':attributeValue, 'sets':sets, 'attributesIndex':attributesIndex}
    print 'Ho deciso il miglior split da fare!'
    return node


#funzione che dato un set di esempi ne calcola l'entropia
def calculateEntropy(examples, classes):
    if(sameClassifcation(examples)):
        return 0.0
    else:
        rows = float(len(examples))
        entropy = 0.0
        examplesClasses = [row[-1] for row in examples]
        for classValue in classes:
            classRows = float(examplesClasses.count(classValue))
            if classRows == 0:
                continue
            entropy = entropy - (classRows / rows) * math.log(float(classRows / rows), 2)
        return entropy


#funzione che calcola l'information gain: dato uno split di un set di esempi, l'information gain e' calcolato come la
#differenza tra l'entropia tra il totale di esempi e la somma pesata delle entropia dei vari split
def calculateInformationGain(sets, classes):
    examples = []
    for set in sets:
        examples = examples + set
    rows = float(len(examples))
    remainder = 0.0
    for set in sets:
        setRows = float(len(set))
        if setRows == 0:
            continue
        remainder = remainder + (setRows / rows) * calculateEntropy(set, classes)
    informationGain = calculateEntropy(examples, classes) - remainder
    return informationGain


# funzione che prende in input un dataset, l'indice di un attributo del dataset e un valore per tale attributo e
# restituisce due liste contenti tutti gli elementi del dataset rispettivamente con valore dell'attributo superiore e
# inferiore rispetto a quello passato
def split(examples, attribute, value):
    sup, inf = [], []
    for row in examples:
        if row[attribute] >= value:
            sup.append(row)
        else:
            inf.append(row)
    return sup, inf


#dato un gruppo di esempi restituisce la clasificazione maggiormente ricorrente in essi
def terminal(group):
    examplesClasses = [row[-1] for row in group]
    return max(set(examplesClasses), key=examplesClasses.count)


#dato un set di esempi verifica se questi appartengo tutti alla stessa classificazione (True) oppure no (False)
def sameClassifcation(examples):
    result = True
    classification = examples[0][-1]
    for row in examples:
        if row[-1] != classification:
            result = False
            break
    return result