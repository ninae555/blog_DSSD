#%%
# Loading the dataset
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

energy_saved = pd.read_csv('../input/singapore-waste-management/waste_energy_stat.csv')
waste_03_17 = pd.read_csv('../input/singapore-waste-management/2003_2017_waste.csv')
waste_18_20 = pd.read_csv('../input/singapore-waste-management/2018_2020_waste.csv')
# %%
