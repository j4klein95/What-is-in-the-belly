import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy import inspect

from flask import Flask, jsonify, render_template, redirect

# Set up connection to database

engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# create references

bacteria = Base.classes.otu
samples = Base.classes.samples
samples_metadata = Base.classes.samples_metadata

#create our session to the db

session = Session(engine)

# Set up flask application

app = Flask(__name__)

@app.route("/")
def dashboard():
    """Return the dashboard homepage."""
    return render_template("index.html")

@app.route("/names")
def names():
    """Return a list of sample names."""
    results = session.query(samples)
    list_names = list(session.execute(results).keys())
    full_name_list = list_names[1:]
    stripped_list = [s.strip('samples_') for s in full_name_list]
    return jsonify(stripped_list)

@app.route("/otu")
def otu_list():
    """Return list of OTU descriptions."""
    results = session.query(bacteria.lowest_taxonomic_unit_found).all()
    descriptions = results
    return jsonify(descriptions)

@app.route("/metadata/<sample>")
def metadata(sample):
    """Returns metadata for a given sample
    Args: Sample in the format:'BB_940'
    returns a json dict of metadata like so:
    {
        Age: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
    y = session.query(samples_metadata.AGE, samples_metadata.BBTYPE, samples_metadata.ETHNICITY, samples_metadata.GENDER, samples_metadata.LOCATION, samples_metadata.SAMPLEID).filter(samples_metadata.SAMPLEID == "BB_" + sample)
    metadata_list = []
    for result in y:
        row = {}
        row["Age"] = result[0]
        row["BBType"] = result[1]
        row["Ethnicity"] = result[2]
        row["Gender"] = result[3]
        row["Location"] = result[4]
        row["SampleID"] = result[5]
        metadata_list.append(row)
    return jsonify(metadata_list)

@app.route('/samples/<sample>')
def samples_id_values(sample):
    """OTU ID's and Sample Values for a given sample.

    sort by Sample Value in descending order, return a list of dictionaries for
    'otu_ids' and 'sample_values'

    [
        {
            otu_ids: [
                1166,
                2858,
            ],
            sample_values: [
                163,
                126,
            ]
        }
    ]
    """

if __name__ == '__main__':
    app.run(debug=True)
