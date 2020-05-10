# Duckworth-Lewis-Stern-Method
By analyzing 1 st innings data you have to build the prediction system for remaining overs and wickets.This is nothing but a Duckworth-Lewis-Stern System.

### •   Brief about this method.

1.  In simple terms, the D/L system converts the number of overs remaining and the number of wickets lost into a "resources remaining" figure.
2.  As overs are completed or wickets fall - the "resources remaining" falls.
3.  When a limited overs cricket match is delayed or interrupted by rain or bad light, there is often insufficient time for both teams to complete their full allocation of overs.
4.  It is therefore necessary to calculate a fair target for the team batting second - taking into account the number of overs that they will face.
5.  Where other earlier methods crucially overlooked the importance of wickets lost at the point of delay, the D/L method incorporates this factor into its calculation. It is obviously much easier to chase 100 runs with ten wickets left than with just three wickets standing and the D/L method was the first of its kind to recognise this.

###### Prediction Formula.

If "v" is the remaining overs and "w" is the wickets in hand,
we would like to predict the runs a team will score by below prediction formula -

R(v, w) = Ro(w) * [1 - exp{ -L * v / Ro(w)}]

Ro is average value when w wickets remaining.


### •   Step 1: Install All the dependencies.

1.  All the dependencies mentioned in requirements.txt
2.  Install using pip install -r requirements.txt

### •   Step 2: Run the application.

1.  Run duckworthlewis.py which will run on http://127.0.0.1:65000.
2.  Visit this URL in web browser.

3.  If you want to run on specific IP then change "host" in duckworthlewis.py
4.  And visit http://IP-ADDRESS:65000.

### •   Step 3: Perform prediction.

1.  Tune L value (train).
2.  Observe graph by clicking view graph.
3.  Now go for prediction.
