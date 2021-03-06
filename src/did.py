# A health provider is interested in studying the effect 
# of a new hospital admissions procedure on patient satisfaction. 
# They have monthly data on patients before and after the new 
# procedure was implemented in some of their hospitals. The data 
# are in nested JSON format, and the health provider uses Python 
# as the data analysis tool. But they would like to use Stata's 
# new DID regression to analyze the effect of the new admissions 
# procedure on the hospitals that participated in the program. 
# The outcome of interest is patient satisfaction, satisfaction_score, 
# and the treatment variable is procedure.
# The data can be found at 
# https://www.stata.com/new-in-stata/pystata/did.json


# Setup Stata from within Python
import stata_setup
stata_setup.config("C:/Program Files/Stata17", "mp")

# Import the json file into a Python dataframe
import urllib.request, json 
from pandas.io.json import json_normalize

with urllib.request.urlopen("https://www.stata.com/new-in-stata/pystata/did.json") as url:
    data = json.loads(url.read().decode())
data = json_normalize(data, 'records', ['hospital_id', 'month'])

# Load Python dataframe into Stata
from pystata import stata
stata.pdataframe_to_data(data, True)

# Run block of Stata code 
stata.run('''
    destring satisfaction_score, replace
    destring hospital_id, replace
    destring month, replace

    gen proc = 0
    replace proc = 1 if procedure == "New"
    label define procedure 0 "Old" 1 "New"
    drop procedure
    rename proc procedure
    label value procedure procedure
    ''', quietly=True)

# Run Stata commands in Python
stata.run('''
        didregress (satisfaction_score) (procedure), ///
                group(hospital_id) time(month)
        ''', echo=True)

# Load Stata saved results to Python
r = stata.get_return()['r(table)']

# Use them in Python
print("\n")
print("The treatment hospitals had a %5.2f-point increase." % (r[0][0]), end=" ")
print("The result is with 95%% confidence interval [%5.2f, %5.2f]." % (r[4][0], r[5][0]))

# Generate Stata graph in Python
stata.run("estat trendplots", echo=True)
stata.run("graph export did.svg, replace", quietly=True)
