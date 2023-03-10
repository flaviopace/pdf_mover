import os
import shutil

startSearchPath = "."
storePath = "./mesure.txt"
pattern_end = ".pdf"
pattern_start = "pg"
dbCompanyFile = "TransFileDatabase.csv"
outDirPathFile = "TransFilesDropBox.txt"

meseArray = { '01': 'Gennaio', '02': 'Febbraio', '03': 'Marzo', '04': 'Aprile', '05': 'Maggio',
         '06': 'Giugno', '07': 'Luglio', '08': 'Agosto', '09': 'Settembre', '10': 'Ottobre',
         '11': 'Novembre', '12': 'Dicembre'}

class FileSearch(object):

    def __init__(self, filepath, pattern_start, pattern_end):
        ''' We have to define some variable for computation '''
        self.startSearchPath = filepath
        self.pattern_start = pattern_start
        self.pattern_end = pattern_end
        self.fileList = []

    def getFileList(self):
        '''Get the list of Files that ends with defined pattern'''
        for root, dirs, files in os.walk(self.startSearchPath):
            # for each file found
            for file in files:
                #select file that ends with desired pattern
                if file.lower().startswith(self.pattern_start) and file.lower().endswith(self.pattern_end):
                    fileIn = os.path.join(root, file)
                    #print("Trovato file: {}".format(fileIn))
                    self.fileList.append(fileIn)

        if not self.fileList:
            raise Exception ("List is Empty")
        return self.fileList

    def printList(self):
        ''' print array file'''
        print(self.fileList)


def getCompanyDetails(inFile=dbCompanyFile):
    compDic = {}
    try:
        f = open(inFile, "r")
    except Exception as e:
        print("Non riesco ad aprire il file {}  - {}", format(inFile, e))
    for line in f:
        if len(line.strip()):
            companyDetail = line.split(",")
            # key = ID, Value = Nome Azienda
            compDic[companyDetail[0]] = companyDetail[1].strip()

    return compDic

def getDeafaultPath(inFile=outDirPathFile):

    try:
        f = open(inFile, "r")
    except Exception as e:
        print("Non riesco ad aprire il file {}  - {}", format(inFile, e))
    for line in f:
        if len(line.strip()):
            return line
        else:
            return None

def decodeFileName(fileName):

    print("Sto processando il file: {}".format(fileName))
    basename = os.path.basename(fileName)
    fileDetails =[]
    # 2-6 -> Client ID
    fileDetails.append(basename[2:6])
    namelen = len(basename.split(".")[0])
    # 10-12 -> Mese
    fileDetails.append(basename[namelen-4:namelen-2])
    # 12-14 -> Anno
    fileDetails.append(basename[namelen-2:namelen])
    return fileDetails;

if __name__ == "__main__":
    print("Scansione della Dir: \t {}".format(startSearchPath))
    print("File Pattern: \t {} * {}".format(pattern_start, pattern_end))
    files = FileSearch(startSearchPath, pattern_start, pattern_end)
    v = files.getFileList()
    files.printList()

    dic = getCompanyDetails()

    print(dic)

    for file in v:
        fileInfo = decodeFileName(file)
        clienteID = fileInfo[0]
        if clienteID in dic.keys():
            clienteName = dic[clienteID]
        else:
            clienteName = None
            print("Cliente ID {} non trovato!!".format(clienteID))
            continue
        mese = fileInfo[1]
        meseNome = meseArray[mese]
        anno = fileInfo[2]
        annoFull = "20" + anno
        print("Cliente ID: \t{}".format(clienteID))
        print("Cliente Nome: \t{}".format(clienteName))
        print("Mese : \t\t\t{}-{}".format(mese, meseNome))
        print("Anno : \t\t\t{}".format(anno))
        newFileName = mese + " " + meseNome + " " + annoFull + ".pdf"
        print("Nuovo File: \t{}".format(newFileName))
        basePath = getDeafaultPath()
        if basePath:
            newPath = os.path.join(getDeafaultPath(), clienteName, "LAVORO", "BUSTE PAGA", annoFull)
            print("Nuovo Path: \t{}".format(newPath))
            if not os.path.isdir(newPath):
                os.makedirs(newPath)
            newFullName =  os.path.join(newPath, newFileName)
            print("Sto copiando il file {} in {}".format(file, newFullName))
            shutil.copy(file, newFullName)
        else:
            print("Non ho trovato un base patch valido!!")
        print("-------------")

