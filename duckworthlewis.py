"""
    This file will predict the runs.
"""
import os
import ast
import numpy as np
from flask import Flask, render_template, request, send_file, jsonify

from utilities.dls import DLS
from utilities.config import INPUT_DATASET, OUTPUT_GRAPH

APP = Flask(__name__, template_folder="frontend")

class DuckworthLewis:
    """
        This class contains all the methods for duckworth lewis.
    """
    @APP.route("/")
    def show_index():
        """
            This method will return index page.
        """
        return render_template("index.html")

    @APP.route("/anuvrat/dls/calculate", methods=["POST"])
    def calculate_values():
        """
            This method will calculate the tuning parameter L.
        """
        result = DLS().main_method()
        if result[1] == 200:
            return jsonify({"message": result[0]})

    @APP.route("/anuvrat/dls/viewgraph", methods=["GET"])
    def view_graphs():
        """
            This method will plot the graph and return graph.
        """
        return send_file(os.path.join(OUTPUT_GRAPH, "dls-output.png"), as_attachment=False, cache_timeout=0)

    @APP.route("/anuvrat/dls/predict", methods=["POST"])
    def predict_runs():
        """
            This method will calculate the tuning parameter L.
        """
        over = int(request.form.get("over"))
        wicket = int(request.form.get("wicket"))

        value_list = None
        with open(os.path.join(INPUT_DATASET, "values"), "r") as file:
            value_list = file.readline()
        value_list = ast.literal_eval(value_list)

        predicted_run = DLS().prediction_function(value_list[wicket-1], over, value_list[10])
        data = f"According to Duckworth Lewis,\nIn remaining {over} overs and {wicket} wickets the estimated score is {int(predicted_run)}"
        return render_template("index.html", data=data, style="display: block;")

if __name__ == "__main__":
    APP.config["CACHE_TYPE"] = "null"
    APP.jinja_env.cache = {}
    APP.run(host="127.0.0.1", port=65000, debug=True, threaded=True)
