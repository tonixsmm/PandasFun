# (more on) ATTRIBUTES
# 1. what is  the type of the attribute (How should it be stored)
# int, float, str
# 2. what is the semantic type (what does the attribute and its values really represent)
# domain knowledge!!!
# 3. what is the attribute measurement scale?
# categorical and continuous (numeric)

# Categorical
# nominal: categorical measurement scale without inherent ordering (ex: names, eyes color, occupation, zip codes)
# ordinal: categorical measurement scale with an inherent ordering (ex: T-shirt sizes, letter grades, etc.)

# Numeric
# ratio-scaled: continuous where 0 means absence (ex: weight - 0kg means absence of weight, 0 degree K means absence of temperature)
# interval: continuous where 0 does not mean absence (ex: 0 degree fahrenheit does not mean absence of temperature)

# noisy v. invalid
# noisy: valid on the measurement scale, but recorded incorrectly
# ex: age distribute, someone who is 18 but was recorded as 81
# invalid: not valid on the measurement scale
# ex: age distribute, someone enters "Bob"

# labeled v. unlabeled (preview for our unit on machine learning)
# labeled data: if there is an attribute (called class) that you are interested in predicting for "unseen" instances
# this is called supervised machine learning, more on this later this semester
# if the class attribute is categorical, it is called a "classification task"
# if the class attribute is numeric, it is called a "regression task"
# unlabeled data: there is no such attribute (you want to predict)
# maybe you want to use data mining to look for trends, groups, associations, outliers, etc.

# PANDAS - "panel data"
# it is a library for data science. it is built on top of numPy
# why pandas? lots of great data science functionality built in like indexing, slicing, cleaning, stats, etc.
# one of major shortcoming of using lists for table is the lack of label-based indexing
# grab a column by name

# there are two main objects for storing data
# 1D list: Series
# 2D list: DataFrame (where each column is a Series)

# SERIES
# there are several ways to make a Series
# from list
import pandas as pd
populations = [737015, 48161, 20926, 1767]
cities = ["Seattle", "Bothell", "Mill Creek", "Ritzville"]
pop_ser = pd.Series(populations)
print(pop_ser)
pop_ser = pd.Series(populations, index=cities)
print(pop_ser)
pop_ser.name = "Population"
print(pop_ser)

# INDEXING
print(pop_ser["Bothell"])
print(pop_ser[["Bothell", "Ritzville"]])
print(pop_ser["Bothell" : "Ritzville"]) # INCLUSIVE of end when using label with pandas
# use i.loc[] for position-based indexing
print(pop_ser.iloc[[1, 3]]) # double brackets because we pass in a sequence of position
print(pop_ser[1:3]) # EXCLUSIVE of end when using position-based

# SUMMARY STATS
print(pop_ser.mean())
print(round(pop_ser.std(), 2))

# We can add new data to a series
# a new key-value pair to a dictionary
pop_ser["Mukilteo"] = 21538
print(pop_ser)

# we can have an empty series
pop_ser2 = pd.Series(dtype=int)
pop_ser2["Mukilteo"] = 21538
print(pop_ser2)

# DATAFRAME
# make a dataframe from a 2D list
twod_list = [["a", 7, 11.1], ["b", 22, 56.3], ["c", 813, 909.99]]
columns_name = ["col1", "col2", "col3"]
rows_name = ["row1", "row2", "row3"]
df = pd.DataFrame(twod_list, columns=columns_name, index=rows_name)
print(df)
#3 columns: "City", "Population", "Class"
# "Class" can be "Large" "Medium" or "Small"
pop_data = [["Seattle", 737015, "Large"],
            ["Bothell", 48161, "Medium"],
            ["Ritzville", 1767, "Small"],
            ["Spokane", 228989, "Large"],]
columns_name = ["City", "Population", "Class"]
pop_df = pd.DataFrame(pop_data, columns=columns_name)
pop_df = pop_df.set_index("City")
print(pop_df)

# INDEXING
pop_ser = pop_df["Population"]
print(pop_ser)
seattle_ser = pop_df.iloc[0]
print(seattle_ser)
seattle_pop = pop_df.iloc[0, 0]
print(seattle_pop)
# use .loc[] for more advanced label indexing
seattle_pop = pop_df.loc["Seattle", "Population"]
print(seattle_pop)

# let's load regions.csv into a dataframe
regions_df = pd.read_csv("regions.csv", index_col=0)
print(regions_df)

# Let's join pop_df with the region_df to produce a third dataframe called merged_df
# We will join in the column they have in common
# ("City"), which also happens to be the index
merged_df = pop_df.merge(regions_df, on="City", how="outer") # how= can be ommited if we just need inner join, meaning only displaying matches
print(type(merged_df))

# we can write a dataframe (and a series) to a file 
merged_df.to_csv("merged.csv")

# data aggregation
# let's split merged_df on "Class" and apply the mean() to all the Population series in the Class subtables and combine the population means into a final series
# 1. split
grouped_by_class = merged_df.groupby("Class")
print(grouped_by_class)
print(grouped_by_class.groups.keys())
large_df = grouped_by_class.get_group("Large")
print(large_df)
print(type(large_df))
# we don't want to hard code extracting each attribute value's dataframes with get_group()
# instead we are gonna write extensible code using a loop
mean_pop_series = pd.Series(dtype=float)
for group_name, group_df in grouped_by_class:
    print(group_name)
    print(group_df)
    # 2. apply
    group_pop_series = group_df["Population"]
    group_pop_mean = group_pop_series.mean()
    print(group_pop_mean)
    #3. combine
    mean_pop_series[group_name] = group_pop_mean
    print("*****")

print("Split - Apply - Combine results:")
print(mean_pop_series)

# smaller way:
mean_pop_series = grouped_by_class["Population"].mean()
print(mean_pop_series)
