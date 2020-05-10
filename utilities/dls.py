"""
    This file will tune constant from dataset.
"""
import os
import shutil
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import minimize

from utilities.config import INPUT_DATASET, OUTPUT_GRAPH, COLUMNS
matplotlib.use('Agg')

class DLS:
    """
        This class contains all the methods for tuning the value.
    """
    @classmethod
    def read_dataset(cls):
        """
            This method will read the dataset and return.
        """
        odi_data = pd.read_csv(os.path.join(INPUT_DATASET, "ODI_data.csv"), usecols=COLUMNS)
        odi_data["Over"] = 50 - odi_data["Over"]
        odi_data = odi_data[odi_data["Innings"] == 1]
        return odi_data

    @classmethod
    def get_average_runs_per_wicket(cls, wicket, odi_data):
        """
            Get mean run scored at when mentioned "wicket" wicket in hand
        """
        return np.mean(odi_data[odi_data["Wickets.in.Hand"] == wicket].groupby("Match")["Runs.Remaining"].max())

    @classmethod
    def prediction_function(cls, Ravg, over_remain, L):
        """
            Below is prediction function which we are going to predict the score.
        """
        return Ravg * (1 - np.exp(-L * over_remain / Ravg))

    @classmethod
    def get_average_maximum_run(cls, odi_data):
        """
            Get the average maximum runs.
        """
        Ravg = [cls.get_average_runs_per_wicket(wicket + 1, odi_data) for wicket in np.arange(10)]
        return Ravg

    @classmethod
    def calculate_error_function(cls, Ravg, data):
        """
            To calculate error and updates the values in BFGS.
        """
        squared_error, lvalue = [], Ravg[10]

        for index, value in enumerate(data[0]):
            predicted_run = cls.prediction_function(Ravg[data[2][index] - 1], data[1][index], lvalue)
            squared_error.append((predicted_run - data[0][index]) ** 2)

        return np.sum(squared_error)

    @classmethod
    def plot_dls(cls, Ravg_final, Ravg_maximum, modified_overs):
        """
            Plot the curves.
        """
        for index, _ in enumerate(range(1, 11)):
            output = 100 * cls.prediction_function(Ravg_final[index], modified_overs, Ravg_final[-1]) / Ravg_maximum
            plt.plot(modified_overs[::-1], output, label = f"{index+1} wicket remaining")
            plt.legend()

        plt.plot(modified_overs, list(range(100, -1, -2)), "#8b008b", linestyle="dashed")
        plt.xlabel("Overs Remaining")
        plt.ylabel("Resource remaining (%)")

        if not os.path.isdir(OUTPUT_GRAPH):
            os.mkdir(OUTPUT_GRAPH)
        else:
            shutil.rmtree(OUTPUT_GRAPH)
            os.mkdir(OUTPUT_GRAPH)

        plt.savefig(os.path.join(OUTPUT_GRAPH, "dls-output.png"))

    @classmethod
    def main_method(cls):
        """
            Entry to this code and this code will call all the necessary methods.
        """
        odi_data = cls.read_dataset()
        Ravg = cls.get_average_maximum_run(odi_data)
        Ravg.append(1) # This is L and initially dummy value "L-BFGS-B" algorithm will calculate optimized value.

        solution = minimize(cls.calculate_error_function, Ravg, method = "L-BFGS-B",
                            args = [odi_data["Runs.Remaining"].values, odi_data["Over"].values, odi_data["Wickets.in.Hand"].values])
        Ravg_final, minimum_loss = solution["x"], solution["fun"]
        with open(os.path.join(INPUT_DATASET, "values"), "w") as file:
            file.write(str(list(Ravg_final)))

        Ravg_maximum = cls.prediction_function(Ravg_final[9], 50, Ravg_final[10])
        cls.plot_dls(Ravg_final, Ravg_maximum, np.arange(51))
        return f"Completed successfully. L = {Ravg_final[-1]}", 200
