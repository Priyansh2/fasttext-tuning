#get all model's folders
addr =outRootAddr
modelsFolders = list(os.listdir(addr))
modelsFolders.sort()
print (modelsFolders)
modelsFolders = [ str(mf) for mf in modelsFolders ]

def parseScores(fileaddr):
    scores = {}
    with open(fileaddr, 'r') as f:
        content = list(f.readlines())
        for line in content:
            temp = line.split('\t')
            scores[temp[0].strip()] = float(temp[1].strip())

    #change it so key is mf, value is another dict without intermediate keys
    def removeSecondLevelIndirectionFromDict(d):
        ret = {}
        for key1 in d: #keep this one
            ret[key1] = {}
            for key2 in d[key1]:
                for key3 in d[key1][key2]:
                    ret[key1][key3] = d[key1][key2][key3]
                
     scores = removeSecondLevelIndirectionFromDict(scores)
     return scores

def parsePars(fileaddr):
    pars = {}
    with open(fileaddr, 'r') as f:
        content = list(f.readlines())
        for line in content:
            temp = line[1:-2]
            temp = temp.split('\\n')
            temp = [ t.strip() for t in temp if t.strip() != '' ]
            for t in temp:
                split = t.split(':')
                pars[split[0].strip()] = split[1].strip()
                try:
                    pars[split[0].strip()] = float(pars[split[0].strip()])
                except:
                    continue
    return pars
    
scores = {} #key: mf (string), value, another dict of scores and their values
pars = {}
for mf in modelsFolders:
    print (mf)
    modelFiles = os.listdir(addr+mf)
    scoreFiles = [ mf for mf in modelFiles if 'At1' in mf and 'test' in mf ] #isolate the test files produced by fasttext which contain the scores, using precisions @1 for now
    scoreFiles.sort()
#     print (scoreFiles)
    parFile = 'parList.txt'
    
    #read scores
    scores[mf] = {}
    for scoreFile in scoreFiles:
        scores[mf][scoreFile] = parseScores(addr+mf+'/'+scoreFile)
         
    #read parameters
    pars[mf] = parsePars(addr+mf+'/'+parFile)
    
parsDf = pd.DataFrame.from_dict(pars, orient='index')
parsDf['mf'] = parsDf.index
parsDf['mf'] = parsDf['mf'].astype(int)
print (parsDf.head())

scoresDf = pd.DataFrame.from_dict(scores, orient='index')
scoresDf['mf'] = scoresDf.index
scoresDf['mf'] = scoresDf['mf'].astype(int)
print (scoresDf.head())

scoresDatabase = pd.merge(parsDf, scoresDf, on="mf")
scoresDatabase.to_csv(addr+'scoresDatabase.csv')
