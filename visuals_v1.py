#%%
# Loading the dataset
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


energy_saved = pd.read_csv('waste_energy_stat.csv')

waste_03_17 = pd.read_csv('2003_2017_waste.csv')
waste_18_20 = pd.read_csv('2018_2020_waste.csv')
# %%
# Print the first 5 rows of energy_saved

energy_saved.head()
#%%
# Print the first 5 rows of waste_03_17

waste_03_17.head()
#%%
# Print the first 5 rows of waste_18_20

waste_18_20.head()

# %%
from functions import null_checker

df_nan = null_checker(energy_saved)

# Print df_nan
# %%
# Plot a line chart to show the trend of total energy saved over the years