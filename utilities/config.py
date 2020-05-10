"""
	Config file which contains constant values.
"""
import os

PATH = os.path.join(os.getcwd(), "utilities")
INPUT_DATASET = os.path.join(PATH, "input_dataset")
OUTPUT_GRAPH = os.path.join(PATH, "output_graph")

COLUMNS = ["Match", "Innings", "Runs.Remaining", "Wickets.in.Hand", "Over", "Innings.Total.Runs"]
