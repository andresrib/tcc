from numpy import size


arquive = "rerrodar_Sensors_1Colision_gn_pista2.txt"
test = 29
generation = [1, 2, 4, 8, 16, 32, 64, 100]

with open(arquive, "r") as arq:
    brute = arq.read()
    separate = brute.split("teste")
    #print(size(separate))
    separatePerGen = separate[test].split("/")
    
    for gen in generation:
        cromossomes = separatePerGen[gen-1].split("\n")
        cromossomes.remove("")
        #gene = cromossomes[1].split(" ")
        #print(cromossomes)
        #print(len(cromossomes[0]))
        #print(gene)
        best = 3600
        #print("best:" + best)
        bestCromossome = cromossomes[0]
        for cromossome in cromossomes:
            if len(cromossome) > 0:
                gene = cromossome.split(" ")
                #print(cromossome)
                #print("aaa")
                if  int(gene[-1]) < int(best):
                    best = gene[-1]
                    bestCromossome = cromossome
                    #print(bestCromossome)
        print(bestCromossome + " " + str(gen))