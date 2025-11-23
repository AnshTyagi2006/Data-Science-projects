import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#         Date       City     Product  Units_Sold  Price_Per_Unit  Discount(%) Salesman
# 0 2025-01-23  Hyderabad      Mobile          60           13701         12.0   Suresh
# 1 2025-01-24      Delhi  Headphones          37            1477          0.0    Priya
# 2 2025-01-24    Kolkata      mobile          52           16762          0.0   Anjali
# 3 2025-01-12     Mumbai      LAPTOP          13           53184          5.0   Rajesh
# 4 2025-01-17     Mumbai      LAPTOP           8           54975          7.0   Suresh
# 5 2025-01-09  Bangalore      LAPTOP           4           56916          0.0    Karan
# 6 2025-01-05    mumbai       LAPTOP           4           53176         15.0   Rajesh
# 7 2025-01-15      Delhi      Laptop          11           56909          5.0   Rajesh
# 8 2025-01-11  Hyderabad     Tablet           22           18495          5.0   Rajesh
# 9 2025-01-03      Delhi     Unknown          91           20194          7.0     Neha
df = pd.read_excel("MATPLOTLIB/Sales_Data_Jan2025_Messy.xlsx")

df["Date"] = pd.to_datetime(df["Date"] , format='mixed' , dayfirst=True , errors="coerce")
df.loc[ (df["Discount(%)"]<0 )| (df["Discount(%)"]>100) | (df["Discount(%)"].isnull()==True) , "Discount(%)"] = 0
df.loc[ (df["Salesman"] == "nan") | (df["Salesman"].isnull()==True) , "Salesman"] = "Unknown"
df.loc[ (df["Product"] == "nan") | (df["Product"].isnull()==True) , "Product"] = "Unknown"
df["City"] = df["City"].str.strip().str.title()
df.loc[(df["City"]=="mumbai"),"City"]="Mumbai"
df.loc[(df["City"]=="New Delhi") | (df["City"]=="delhi"),"City"]="Delhi"
df.loc[(df["City"]=="HYDERABAD"),"City"]="Hyderabad"
df.loc[(df["City"]=="kolkata"),"City"]="Kolkata"

df.loc[(df["City"] == "nan") | (df["City"].isnull()==True) , "City"] = "Unknown"

df = df.drop(df[(df["Units_Sold"] <= 0) | (df["Price_Per_Unit"] <= 0)].index)
df["Price_Per_Unit"] = pd.to_numeric(df["Price_Per_Unit"] , errors='coerce')
df["Product"] = df["Product"].str.strip().str.title().str.replace(' ','')
df.loc[df["Product"] =="HeadPhones","Product"] = "Headphones"
df.drop_duplicates()

totalprice = df["Units_Sold"] * df["Price_Per_Unit"] * ( 1 - df["Discount(%)"] /100)
df.insert( 6 , "TotalPrice" , totalprice)
print(df.head(5))

dates = {
    "Year" : df["Date"].dt.year,
    "Month" : df["Date"].dt.month,
    "Day":df["Date"].dt.day,
}
df1 = pd.DataFrame(dates)
print(f"\nOrder Dates : \n{df1.head(5)}")

cities = df.groupby("City")["TotalPrice"].sum()
print(f"\nTotal Sales per city : \n{cities} ")

products = df.groupby("Product")["TotalPrice"].sum()
print(f"\nTotal Sales per product : \n{products} ")

salesman = df.groupby("Salesman")["TotalPrice"].sum()
print(f"\nTotal Sales per salesman : \n{salesman} ")

hightrans = df.sort_values(by="TotalPrice" , ascending=False ).head(5)
print(f"\nTop 5 highest transactions : \n{hightrans}")

maxsale = df.groupby("Salesman")["TotalPrice"].sum()
salesman_maxsale = maxsale.idxmax()
print(f"\n {salesman_maxsale} has generated maximum sales of {maxsale.max()} in Janurary 2025")

fig , ax = plt.subplots( 1,2 , figsize=(10,5))
ax[0].bar(df["City"],df["TotalPrice"],
        color="#0695F5",
        alpha=1,
        label="Sales by city")
ax[0].set_title("Sales by city")
ax[0].set_xlabel("City")
ax[0].set_ylabel("Sales")
ax[0].grid(True,color="grey",linestyle=":",alpha=0.5)
ax[0].legend()

ax[1].bar(df["Product"],df["TotalPrice"],
        color="#F50652",
        alpha=1,
        label="Sales by Product")
ax[1].set_title("Product sales")
ax[1].set_xlabel("Product")
ax[1].set_ylabel("Sales")
ax[1].grid(True,color="grey",linestyle=":",alpha=0.5)
ax[1].legend()
plt.suptitle("Data Insights")
plt.show()
df=df.sort_values("Date")
plt.plot(df["Date"].dt.day ,df["TotalPrice"],
        color="#7D06F5",
        alpha=1,
        marker="o",
        linewidth=2,
        label="Daily sales",
        )
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Sales")
ax = plt.gca()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
plt.gcf().autofmt_xdate()
plt.grid(True,color="grey",linestyle=":",alpha=0.5)
plt.legend()


plt.show()







