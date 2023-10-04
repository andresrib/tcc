import os
from numpy import size
import pandas as pd
import matplotlib.pyplot as plt


arquives = os.listdir(".")

best_counter = 0
generations_counter = 0
splitten_result = []
for arquive in arquives:
    if "fitness" in arquive and "exploit" not in arquive:
        with open(arquive, "r") as fitness:
            separate = fitness.read().split("melhor e media")
            separate.remove('')
            for result in  separate:
                if "pista0" in arquive:
                    if "1641" in result:
                        best_counter += 1
                        splitten_result = result.split("1641")
                        generations_counter += splitten_result[0].count("\t")                       
                elif "pista1" in arquive:
                    if "1120" in result:
                        best_counter += 1
                        splitten_result = result.split("1120")
                        generations_counter += splitten_result[0].count("\t")
                elif "pista2" in arquive:
                    if "1543" in result:
                        best_counter += 1
                        splitten_result = result.split("1543")
                        generations_counter += splitten_result[0].count("\t")
            """if "pista0" in arquive:
                if "1641" in result:
                    splitten_result = result.split("1641")
                    print(splitten_result[0])
                    print(arquive + ": " + str(splitten_result[0].count("\t")))
                    generations_counter += splitten_result[0].count("\n")  
            elif "pista1" in arquive:
                if "1120" in result:
                    splitten_result = result.split("1120")
                    print(splitten_result[0])
                    print(arquive + ": " + str(splitten_result[0].count("\t")))
                    generations_counter += splitten_result[0].count("\n")  
            elif "pista2" in arquive:
                if "1543" in result:
                    splitten_result = result.split("1543")
                    print(splitten_result[0])
                    print(arquive + ": " + str(splitten_result[0].count("\t")))
                    generations_counter += splitten_result[0].count("\n")"""
            #print(splitten_result[0])
            #print("aaa:" + str(generations_counter))
            
            
            #print(str(size(separate)))
            if best_counter > 0:
                generations_medium = generations_counter/best_counter
            else:
                generations_medium = 0
            print(arquive + " " + str(best_counter) + " " + str(best_counter/size(separate)*100) + "%" + " " + str(generations_medium) + "\n")
            generations_counter = 0
            best_counter = 0
            