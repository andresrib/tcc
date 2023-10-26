#encoding: utf-8
import os
from numpy import size
import pandas as pd
import matplotlib.pyplot as plt
import random
import xlsxwriter


arquives = os.listdir(".")
#arquives = ["rerrodar_1Lap_initial_fitness_pista0.txt"]

best_counter = 0
generations_counter = 0
categories = ["melhor", "média"]
#best_fitness = 3600
#best = []
for arquive in arquives:
    if "fitness" in arquive and "exploit" not in arquive and "initial" in arquive:
        best = []
        best_fitness = 3600
        with open(arquive, "r") as fitness:
            separate = fitness.read().split("melhor e media")
            for _ in separate:
                if '' in separate:
                    separate.remove('')
            test_counter = 0
            best_number = []
            for test in separate:
                test_counter += 1
                generation = test.split("\n")
                for _ in generation:
                    if '' in generation:
                        generation.remove('')
                last_gen = generation[-1].split('\t')
                if int(last_gen[0]) < int(best_fitness):
                    best = [test]
                    best_fitness = last_gen[0]
                    best_number = [test_counter]
                elif int(last_gen[0]) == int(best_fitness):
                    best.append(test)
                    best_fitness = last_gen[0]
                    best_number.append(test_counter)
            test_counter = 0
            print(arquive + ": " + str(size(best)))
            for test in best:
                print("aaaa")
                generation = test.split("\n")
                for _ in generation:
                    if '' in generation:
                        generation.remove('')
                for gen in generation:
                    if '' in generation:
                        generation.remove('')
                
                melhor = []
                media = []
                for gen in generation:
                    isolated_value = gen.split('\t')
                    melhor.append(int(isolated_value[0]))
                    media.append(int(isolated_value[1]))
                df = pd.DataFrame({"melhor": melhor, "media": media}, index= None)
                
                x = arquive.replace(".txt", "")
                x  = x.replace("Colision", "C")
                y = x.replace("rerrodar_", "")
                
                sheet_name = y.replace("fitness", "") + "_" + str(best_number[test_counter])
                writer = pd.ExcelWriter("./excel/" + sheet_name +".xlsx", engine="xlsxwriter")
                df.to_excel(writer, sheet_name=sheet_name)
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]
                (max_row, max_col) = df.shape
                chart = workbook.add_chart({"type": "line"})
                
                chart.add_series(
                    {
                        "name": [sheet_name, 0, 1],
                        "values": [sheet_name, 1, 1, max_row, 1],
                    }
                )
                chart.add_series(
                    {
                        "name": [sheet_name, 0, 2],
                        "values": [sheet_name, 1, 2, max_row, 2],
                    }
                )
                chart.set_x_axis({"name": "Gerações"})
                chart.set_y_axis({"name": "Fitness", "major_gridlines": {"visible": False}})
                worksheet.insert_chart(1, 6, chart)
                writer.close()
                test_counter +=1
                #exit()
