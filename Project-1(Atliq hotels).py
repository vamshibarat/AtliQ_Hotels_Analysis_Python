#!/usr/bin/env python
# coding: utf-8

# In[ ]:


<h2 align="center">AtliQ Hotels Data Analysis Project<h2>


# In[5]:


import pandas as pd


# In[ ]:


***
### ==> 1. Data Import and Data Exploration
***


# In[ ]:


### Datasets
We have 5 csv file 

   - dim_date.csv  
   - dim_hotels.csv
   - dim_rooms.csv
   - fact_aggregated_bookings
   - fact_bookings.csv


# In[ ]:


**Read bookings data in a datagrame**


# In[6]:


df_bookings = pd.read_csv("datasets/fact_bookings.csv")
df_bookings.head(4)


# In[7]:


df_bookings.shape


# In[8]:


df_bookings.room_category.unique()


# In[9]:


df_bookings.booking_platform.unique()


# In[10]:


df_bookings.booking_platform.value_counts()


# In[11]:


df_bookings.booking_platform.value_counts().plot(kind="barh")


# In[12]:


df_bookings.describe()


# In[13]:


df_bookings.revenue_generated.min(),df_bookings.revenue_generated.max()


# In[14]:


df_date = pd.read_csv("datasets/dim_date.csv")
df_hotels = pd.read_csv("datasets/dim_hotels.csv")
df_rooms = pd.read_csv("datasets/dim_rooms.csv")
df_agg_bookings = pd.read_csv("datasets/fact_aggregated_bookings.csv")


# In[15]:


df_hotels.shape


# In[16]:


df_hotels.head(4)


# In[17]:


df_hotels.category.value_counts()


# In[78]:


df_hotels.city.value_counts().sort_values().plot(kind="barh")


# In[ ]:


***
**Exercise: Explore aggregate bookings**
***


# In[18]:


df_agg_bookings.head(3)


# In[ ]:


**Exercise-1. Find out unique property ids in aggregate bookings dataset**


# In[20]:


df_agg_bookings.property_id.unique()


# In[21]:


**Exercise-2. Find out total bookings per property_id**


# In[22]:


df_agg_bookings.groupby("property_id")["successful_bookings"].sum()


# In[ ]:


**Exercise-3. Find out days on which bookings are greater than capacity**


# In[23]:


df_agg_bookings[df_agg_bookings.successful_bookings>df_agg_bookings.capacity]


# In[ ]:


**Exercise-4. Find out properties that have highest capacity**


# In[24]:


df_agg_bookings.capacity.max()


# In[ ]:


***
### ==> 2. Data Cleaning
***


# In[25]:


df_bookings.describe()


# In[ ]:


**(1) Clean invalid guests**


# In[26]:


df_bookings[df_bookings.no_guests<=0]


# In[ ]:


As you can see above, number of guests having less than zero value represents data error. We can ignore these records.


# In[27]:


df_bookings=df_bookings[df_bookings.no_guests>0]


# In[28]:


df_bookings.shape


# In[ ]:


**(2) Outlier removal in revenue generated**


# In[29]:


df_bookings.revenue_generated.min(),df_bookings.revenue_generated.max()


# In[30]:


avg,std = df_bookings.revenue_generated.mean(),df_bookings.revenue_generated.std()
avg,std


# In[31]:


higherlimit = avg+3*std


# In[32]:


higherlimit


# In[33]:


lowerlimit = avg-3*std
lowerlimit


# In[34]:


df_bookings[df_bookings.revenue_generated<0]


# In[35]:


df_bookings[df_bookings.revenue_generated>higherlimit]


# In[36]:


df_bookings=df_bookings[df_bookings.revenue_generated<higherlimit]


# In[37]:


df_bookings


# In[38]:


df_bookings.revenue_realized.describe()


# In[39]:


higher_limit = df_bookings.revenue_realized.mean() + 3*df_bookings.revenue_realized.std()
higher_limit


# In[40]:


df_bookings[df_bookings.revenue_realized>higher_limit]


# In[ ]:


One observation we can have in above dataframe is that all rooms are RT4 which means presidential suit. Now since RT4 is a luxurious room it is likely their rent will be higher. To make a fair analysis, we need to do data analysis only on RT4 room types


# In[41]:


df_bookings[df_bookings.room_category=="RT4"].revenue_realized.describe()


# In[42]:


# mean + 3*standard deviation
23439+3*9048


# In[ ]:


Here higher limit comes to be 50583 and in our dataframe above we can see that max value for revenue realized is 45220. Hence we can conclude that there is no outlier and we don't need to do any data cleaning on this particular column


# In[43]:


df_bookings.isnull().sum()


# In[ ]:


Total values in our dataframe is 134576. Out of that 77899 rows has null rating. Since there are many rows with null rating, we should not filter these values. Also we should not replace this rating with a median or mean rating etc


# In[ ]:


**Exercise-1. In aggregate bookings find columns that have null values. Fill these null values with whatever you think is the appropriate subtitute (possible ways is to use mean or median)**


# In[44]:


df_agg_bookings.isnull().sum()


# In[45]:


df_agg_bookings[df_agg_bookings.capacity.isna()]


# In[46]:


df_agg_bookings.capacity.median()


# In[47]:


df_agg_bookings.capacity.fillna(df_agg_bookings.capacity.median(), inplace=True)


# In[48]:


df_agg_bookings.loc[[8,14]]


# In[ ]:


**Exercise-2. In aggregate bookings find out records that have successful_bookings value greater than capacity. Filter those records**


# In[49]:


df_agg_bookings[df_agg_bookings.successful_bookings>df_agg_bookings.capacity]


# In[50]:


df_agg_bookings.shape


# In[51]:


df_agg_bookings = df_agg_bookings[df_agg_bookings.successful_bookings<=df_agg_bookings.capacity]
df_agg_bookings.shape


# In[ ]:


***
### ==> 3. Data Transformation
***


# In[ ]:


**Create occupancy percentage column**


# In[52]:


df_agg_bookings['occ_pct'] = df_agg_bookings['successful_bookings']/df_agg_bookings['capacity']


# In[53]:


df_agg_bookings.head()


# In[54]:


df_agg_bookings['occ_pct'] = df_agg_bookings['occ_pct'].apply(lambda x: round(x*100, 2))
df_agg_bookings.head(3)


# In[55]:


df_agg_bookings.info()


# In[ ]:


There are various types of data transformations that you may have to perform based on the need. Few examples of data transformations are,

Creating new columns
Normalization
Merging data
Aggregation


# In[ ]:


***
### ==> 4. Insights Generation
***


# In[56]:


df_agg_bookings.head(3)


# In[ ]:


**1. What is an average occupancy rate in each of the room categories?**


# In[57]:


df_agg_bookings.groupby("room_category")["occ_pct"].mean().round(2)


# In[58]:


df_rooms


# In[59]:


df = pd.merge(df_agg_bookings, df_rooms, left_on="room_category", right_on="room_id")
df.head(4)


# In[64]:


df.groupby("room_class")["occ_pct"].mean().round(2)


# In[65]:


df.drop("room_id",axis=1, inplace=True)
df.head(4)


# In[ ]:


**2. Print average occupancy rate per city**


# In[66]:


df_hotels.head(3)


# In[67]:


df = pd.merge(df, df_hotels, on="property_id")
df.head(3)


# In[132]:


df.groupby("city")["occ_pct"].mean().round(2).plot(kind="barh")


# In[ ]:


**3. When was the occupancy better? Weekday or Weekend?**


# In[133]:


df_date.head(3)


# In[134]:


df = pd.merge(df, df_date, left_on="check_in_date", right_on="date")
df.head(3)


# In[135]:


df.groupby("day_type")["occ_pct"].mean().round(2)


# In[139]:


df["mmm yy"].unique()


# In[ ]:


**4: In the month of June, what is the occupancy for different cities**


# In[137]:


df_june_22 = df[df["mmm yy"]=="Jun 22"]
df_june_22.head(4)


# In[140]:


df_june_22.groupby('city')['occ_pct'].mean().round(2).sort_values(ascending=False)


# In[141]:


df_june_22.groupby('city')['occ_pct'].mean().round(2).sort_values(ascending=False).plot(kind="bar")


# In[ ]:


**5: We got new data for the month of august. Append that to existing data**


# In[142]:


df_august = pd.read_csv("datasets/new_data_august.csv")
df_august.head(3)


# In[143]:


df_august.columns


# In[144]:


df.columns


# In[145]:


df_august.shape


# In[146]:


df.shape


# In[147]:


latest_df = pd.concat([df, df_august], ignore_index = True, axis = 0)
latest_df.tail(10)


# In[148]:


latest_df.shape


# In[ ]:


**6. Print revenue realized per city**


# In[68]:


df_bookings.head()


# In[69]:


df_hotels.head(3)


# In[81]:


df_bookings_all = pd.merge(df_bookings, df_hotels, on="property_id")
df_bookings_all.head(3)


# In[82]:


df_bookings_all.groupby("city")["revenue_realized"].sum().sort_values(ascending=False)


# In[ ]:


**7. Print month by month revenue**


# In[73]:


df_date.head(3)


# In[74]:


df_date["mmm yy"].unique()


# In[155]:


df_bookings_all.head(3)


# In[75]:


df_date.info()


# In[86]:


df_date["date"] = pd.to_datetime(df_date["date"])
df_date.head(3)


# In[87]:


df_bookings_all.info()


# In[88]:


df_bookings_all["check_in_date"] = pd.to_datetime(df_bookings_all["check_in_date"])
df_bookings_all.head(4)


# In[89]:


df_bookings_all = pd.merge(df_bookings_all, df_date, left_on="check_in_date", right_on="date")
df_bookings_all.head(3)


# In[93]:


df_bookings_all.groupby("mmm yy")["revenue_realized"].sum().sort_values(ascending=False)


# In[ ]:


**Exercise-1. Print revenue realized per hotel type**


# In[165]:


df_bookings_all.property_name.unique()


# In[95]:


df_bookings_all.groupby("property_name")["revenue_realized"].sum().round(2).sort_values(ascending=False)


# In[ ]:


**Exercise-2 Print average rating per city**


# In[97]:


df_bookings_all.groupby("city")["ratings_given"].mean().round(2).sort_values(ascending=False)


# In[ ]:


**Exercise-3 Print a pie chart of revenue realized per booking platform**


# In[167]:


df_bookings_all.groupby("booking_platform")["revenue_realized"].sum().plot(kind="pie")

