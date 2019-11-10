#Imports



#Codes

def wordyfile(filepath):
    file =  open(filepath,"r")



    #İşlenmiş veri gelmesi gerekiyor bunu önceden işlenecek şey eklenecek
    lines = file.readlines()
    returnlist = list()
    for line in lines:
        line = line.split(",")
        for i in line:
            returnlist.append(i)
    
    file.close()
    return returnlist