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

clean_waste_18_20 = waste_18_20.rename(columns={
        "Waste Type": "waste_type",
        "Total Generated ('000 tonnes)": "total_waste_generated_tonne",
        "Total Recycled ('000 tonnes)": "total_waste_recycled_tonne",
        "Year": "year",
    }).assign(
        total_waste_generated_tonne=lambda df: df["total_waste_generated_tonne"] * 1000,
        total_waste_recycled_tonne=lambda df: df["total_waste_recycled_tonne"] * 1000
    )


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
columns_to_keep = [
    "waste_type",
    "total_waste_generated_tonne",
    "total_waste_recycled_tonne",
    "recycling_rate",
    "year"
]

clean_waste_03_17 = waste_03_17.loc[:, columns_to_keep].copy()

# %%
clean_waste_18_20 = clean_waste_18_20.assign(
    recycling_rate=clean_waste_18_20["total_waste_recycled_tonne"] / clean_waste_18_20["total_waste_generated_tonne"]
)
clean_waste_18_20["recycling_rate"] = clean_waste_18_20["recycling_rate"].round(2)

# %%
clean_waste_18_20.head()

#%%
clean_waste_03_17.head()

#%%
processed_df.head()

#%%
import plotly.express as px
import plotly.graph_objects as go

data = pd.concat([clean_waste_18_20, clean_waste_03_17]).sort_values(by="year")
overall = data[(data["waste_type"] == "Overall") | (data["waste_type"] == "Total")]

fig = go.Figure()

# Add lines for total waste generated and total waste recycled
fig.add_trace(go.Scatter(x=overall["year"], y=overall["total_waste_generated_tonne"],
                         mode='lines', name='Total Waste Generated',
                         line=dict(color='rgba(31, 119, 180, 0.8)')))

fig.add_trace(go.Scatter(x=overall["year"], y=overall["total_waste_recycled_tonne"],
                         mode='lines', name='Total Waste Recycled',
                         line=dict(color='rgba(255, 127, 14, 0.8)')))

fig.update_layout(title="Overall Waste Generation and Recycling Over the Years",
                  xaxis_title="Year", yaxis_title="Waste (tonnes)",
                  legend_title="Type")

# Save the figure as an HTML file
fig.write_html("visualization.html")




# %%
replace_dict = {
    "Non-ferrous metal": "Non-Ferrous Metal",
    "Non-ferrous metals": "Non-Ferrous Metal",
    "Non-Ferrous Metals": "Non-Ferrous Metal",
    "Plastics": "Plastic",
    "Ferrous metal": "Ferrous Metal",
    "Paper/Cardboard": "Paper"
}

data["waste_type"] = data["waste_type"].replace(replace_dict)

#%%

clean_energy_saved = (
    energy_saved.T.iloc[1:, 2:]
    .reset_index(drop=True)
    .rename(columns={2: "material", 3: "energy_saved", 4: "crude_oil_saved"})
)

clean_energy_saved["energy_saved"] = clean_energy_saved["energy_saved"].str.replace("kWh", "").str.replace("Kwh", "")

clean_energy_saved["energy_saved"] = clean_energy_saved["energy_saved"].astype(int)

clean_energy_saved



# %%
total_data = data.merge(clean_energy_saved, how="left", left_on="waste_type", right_on="material").dropna()

total_data["energy_saved"] = total_data["energy_saved"].astype(int)

total_data.head()


# %%
total_data["total_energy_saved"] = total_data["total_waste_recycled_tonne"] * total_data["energy_saved"]

total_data.head()

# %%
# Sunburst Chart
import plotly.io as pio
import plotly.graph_objects as go

# Function to format numbers with B for billion and M for million
def format_number(value):
    if value >= 1e9:
        return f'{value / 1e9:.1f}B'
    elif value >= 1e6:
        return f'{value / 1e6:.1f}M'
    else:
        return str(value)

# Calculate the total energy saved for each material
total_energy_by_material = total_data.groupby('material')['total_energy_saved'].sum().reset_index()

fig = go.Figure(go.Sunburst(
    labels=total_energy_by_material['material'],
    parents=[''] * len(total_energy_by_material),
    values=total_energy_by_material['total_energy_saved'],
    hovertemplate='<b>%{label}</b><br>Total Energy Saved: %{customdata}',
    customdata=[format_number(value) for value in total_energy_by_material['total_energy_saved']],
))

fig.update_layout(title='Material Breakdown',
                  height=600,
                  width=600)

pio.write_html(fig, "visualization2.html")




# %%
# Energy saved per year

annual_energy_savings = total_data.groupby("year").sum().reset_index()
annual_energy_savings["total_energy_saved"] = (annual_energy_savings["total_energy_saved"] / 1000000).round(2).astype(str) + " GWh"
annual_energy_savings = annual_energy_savings.astype({"total_energy_saved": str})

annual_energy_savings.tail()


# %%
