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

data = pd.concat([clean_waste_18_20, clean_waste_03_17]).sort_values(by="year")
overall = data[(data["waste_type"] == "Overall") | (data["waste_type"] == "Total")]

fig = px.bar(overall, x="year", y=["total_waste_generated_tonne", "total_waste_recycled_tonne"],
             barmode="group", labels={"value": "Waste (tonnes)", "variable": "Type"})

fig.update_layout(title="Overall Waste Generation and Recycling Over the Years",
                  xaxis_title="Year", yaxis_title="Waste (tonnes)",
                  legend_title="Type")

import plotly.io as pio

# Save the figure as an HTML file
pio.write_html(fig, "visualization.html")



# %%
import plotly.graph_objects as go
import plotly.io as pio

# Create a line plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=overall["year"],
        y=overall["total_waste_generated_tonne"],
        mode='lines',
        name='Waste Generated'
    )
)

fig.add_trace(
    go.Scatter(
        x=overall["year"],
        y=overall["total_waste_recycled_tonne"],
        mode='lines',
        name='Waste Recycled'
    )
)

# Customize the layout
fig.update_layout(
    title='Waste Generated and Recycled Over the Years',
    xaxis_title='Year',
    yaxis_title='Amount (tonnes)',
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    legend=dict(
        x=0.8,
        y=0.95,
        bgcolor='white',
        bordercolor='black',
        borderwidth=1
    )
)

# Save the figure as an HTML file
pio.write_html(fig, "visualization.html")



# %%
