import pandas as pd
import glob

############ COMBINING MULTILE CSV FILES #################

csv_files = glob.glob("../data/ProductsData/*.csv")  # Change this path
dfs = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(dfs, ignore_index=True)
merged_df.to_csv("../data/ProductsData/merged_output.csv", index=False)

print("Merged CSV saved as 'merged_output.csv'")
##########################################################
