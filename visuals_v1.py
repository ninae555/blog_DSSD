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


#%%
import math

def null_checker(variable):
    if variable is None:
        print("Variable is null.")
    elif isinstance(variable, float) and math.isnan(variable):
        print("Variable contains NaN.")
    else:
        print("Variable is not null and does not contain NaN.")



# %%
# from functions import null_checker

df_nan = null_checker(energy_saved)


# %%
# Plot a line chart to show the trend of total energy saved over the years

#%%
# Transpose the DataFrame
transposed_df = energy_saved.T

# Remove the first row and first two columns
processed_df = transposed_df.iloc[1:, 2:]

# Reset the index
processed_df = processed_df.reset_index(drop=True)

# Rename the columns
processed_df = processed_df.rename(columns={2: "material", 3: "energy_saved", 4: "crude_oil_saved"})

# Print the processed DataFrame
print(processed_df)

# %%
