import argparse
import pandas as pd
import json
import glob

parser = argparse.ArgumentParser()
parser.add_argument(  dest="filename", type=str, help="filename of data to compute")
parser.add_argument("-e", "--edge",  dest="type_is_edge", action="store_true", help="choose the filetype to compute (-e if edge, nothing if agent)")

args = parser.parse_args()

if args.type_is_edge:
    raise NotImplementedError("Edge results compute is not Implemented yet")


def generate_json(filename):
    json_ = dict()
    
    df = pd.read_csv(filename)
    def create_has_moved(row):
        if row["Step"] == 0:
            return row["Distance Traveled"]
        return row["Distance Traveled"] - df[(row["Step"]-1 == df["Step"]) & (row["Name"] == df["Name"])]["Distance Traveled"].iloc[0]

    step_duration = df["Step Duration"].iloc[0]
    last_step_df = df[df["Step"] == df["Step"].max()]
    df["distance_travelled"] = df.apply(create_has_moved, axis=1)
    df["emission_step"] = df["Distance Traveled"] * df["Emission By Kilometer (running)"] / 1000

    for agent in last_step_df["Name"].unique():
        json_[agent] = dict()
        json_[agent]["total_distance"] = float(last_step_df[last_step_df["Name"] == agent]["Distance Traveled"].iloc[0])
        json_[agent]["total_time"] = float(df[(df["Name"] == agent) & (df["Has Arrived"] == True)]["Step"].iloc[0] * step_duration)
        json_[agent]["time_by_distance"] = float(json_[agent]["total_time"] / json_[agent]["total_distance"])
        json_[agent]["time_wo_stop"] = float((json_[agent]["total_time"] - df[(df["Name"] == agent) & (df["distance_travelled"] == 0.0) & (df["Has Arrived"] == False)]["Step Duration"].sum()) / json_[agent]["total_distance"])
        json_[agent]["total_emission"] = float(df[df["Name"] == agent]["emission_step"].sum() + df[(df["Name"] == agent) & (df["distance_travelled"] == 0.0)]["Emission By Minute (idle)"].sum() / (60 / step_duration))
        json_[agent]["emission_by_distance"] = float(json_[agent]["total_emission"] / json_[agent]["total_distance"])
        json_[agent]["total_consumption"] = float(json_[agent]["total_distance"] * df[df["Name"] == agent]["Consumption"].iloc[0])
        

    max_time = float(max([json_[a]["total_time"] for a in json_]))
    max_time_by_distance = float(max([json_[a]["time_by_distance"] for a in json_]))
    max_time_wo_stop = float(max([json_[a]["time_wo_stop"] for a in json_]))

    json_["max_time"] = max_time
    json_["max_time_by_distance"] = max_time_by_distance
    json_["max_time_wo_stop"] = max_time_wo_stop

        
    json_formated = json.dumps(json_)

    new_filename = filename.split(".")[-2] + ".json"
    with open(new_filename, "w") as f:
        f.write(json_formated)
    
    
    
for file in glob.glob(args.filename):
    print("Genration json file: " + file)
    generate_json(file)
