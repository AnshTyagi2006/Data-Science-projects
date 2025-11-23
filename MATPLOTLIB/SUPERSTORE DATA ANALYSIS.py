import pandas as pd
import matplotlib.pyplot as plt
#1. => DATA READING
df = pd.read_csv("MATPLOTLIB/Super_store_dataset.csv")

#2. => DATA CLEANING
df.dropna()
#1.date formating
df[["Order.Date" , "Ship.Date"]] = df[["Order.Date" , "Ship.Date"]].apply(pd.to_datetime)
#2.remove duplicates
df.drop_duplicates()
#3.standradize columns
df.columns = df.columns.str.replace("." , "")
#4.extracting year,month,weekday from order.date
order_year = df["OrderDate"].dt.year
order_month = df["OrderDate"].dt.month
order_day = df["OrderDate"].dt.day
print(df.head())

#3. => DATA ANALYSIS
#1.total sales , average profit and discount per year
Yearly_summary = df.groupby("Year").agg(
    Totalsales = ("Sales" , "sum"),
    AverageProfit = ("Profit" , "mean"),
    AverageDiscount = ("Discount" , "mean")
)
print(f"\nYearly summary : \n{Yearly_summary}")

#2.Top 10 costumers with max sales
costumer_sales = df.groupby("CustomerName")["Sales"].sum()
max_costumer_sales = costumer_sales.sort_values(ascending=False)
max_sales = max_costumer_sales.head(10)
print(f"\nTop 10 costumers by sales : \n{max_sales}")

#3. Regional , state , city wise sales
Regional_sales = df.groupby("Region")["Sales"].sum()
State_sales = df.groupby("State")["Sales"].sum()
City_sales = df.groupby("City")["Sales"].sum()
print(f"\n Regional sales : \n{Regional_sales}")
print(f"\n State wise sales : \n{State_sales}")
print(f"\nCity wise sales : \n{City_sales}")

#4. Category v/s sub-cateogry sales
category_sales = df.groupby("Category")["Sales"].sum()
subcategory_sales = df.groupby("SubCategory")["Sales"].sum()
print(f"\nCategory wise sales : \n{category_sales.sort_values(ascending = False)}")
print(f"\nSubCategory wise sales : \n{subcategory_sales.sort_values(ascending = False)}")

#5. Monthly sales per year
yearly_sales = df.groupby(["Year" , order_month])["Sales"].sum().reset_index()
print(f"\nMonthly Sales per year : \n{yearly_sales}")

#6.Impact of discount on sales and profit
discount_correlation = df[["Discount", "Sales", "Profit"]].corr()
print(f"\nImpact of dicount on profit and sales : \n{discount_correlation}")

#7. Average shippment time
ship_time = df["ShipDate"] - df["OrderDate"]
print(f"\nAverage shipment time : {ship_time.dt.days.mean().round(0)} days")

#8. Sales v/s Shipping cost relation
cost_correlation = df[["Sales" , "ShippingCost"]].corr()
print(f"\n Sales v/s Shipping cost relation : \n{cost_correlation}")

#9. Order priority with maximum sales
priority_sales = df.groupby("OrderPriority")["Sales"].sum()
max_priority_sales = priority_sales.idxmax()
print(f"\n{max_priority_sales} order priority has the maximum sales of {priority_sales.max()}")

#10. Products wiht -ve profit
df1 = df.loc[ (df["Profit"] < 0) , "SubCategory"].unique()
print("\nProducts with negative profit : ",df1)

#4. => DATA VISUALIZATION
#1.Bar graphs
plt.bar( category_sales.index , category_sales.values,
        color = "#0E7EF6",
        edgecolor = 'black',
        linewidth = 0.5,
        alpha = 1,
        label = "Category sales")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.title("Sales by Category")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

plt.bar( subcategory_sales.index , subcategory_sales.values,
        color = "#5B0EF6",
        edgecolor = 'black',
        linewidth = 0.5,
        alpha = 1,
        label = "SubCategory sales")
plt.xlabel("SubCategory")
plt.ylabel("Sales")
plt.title("Sales by SubCategory")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

plt.bar( Regional_sales.index , Regional_sales.values,
        color = "#54EE40",
        edgecolor = 'black',
        linewidth = 0.5,
        alpha = 1,
        label = "Regional sales")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.title("Region wise sales")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

# #2.line charts
df["OrderYear"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.month
montly_sales = df.groupby(["OrderYear" , "Month"])[["Sales" , "Profit"]].sum().round(0).reset_index()
montly_sales["Month_Year"] = montly_sales["OrderYear"].astype(str) + "-" + montly_sales["Month"].astype(str).str.zfill(2)

plt.plot(montly_sales["Month_Year"], montly_sales["Sales"],
         color="#9806F3", linestyle="-", marker="o", linewidth=2, label="Monthly Sales")
plt.plot(montly_sales["Month_Year"], montly_sales["Profit"],
         color="#05DAFB", linestyle="-", marker="o", linewidth=2, label="Monthly Profit")
plt.xlabel("Month-Year")
plt.ylabel("Sales - Profit")
plt.title("Monthly Sales & profit trend over years.")
plt.legend()
plt.xticks(rotation = 45)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

# 3.Pie charts
segment_sales = df.groupby("Segment")["Sales"].sum()
color = ["skyblue" , "gold" , "purple" , "lightgreen" , "blue" , "gold" , "ceyan"]
plt.pie( segment_sales.values , labels = segment_sales.index , 
        autopct = '%1.1f%%',
        colors = color[ : len(segment_sales)],
        startangle=90,
        frame=True
)
plt.title("Sales share by each segment")     
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

# 4. Scatter plots
df1 = df[(df["Sales"] < 5000) & (df["Profit"] < 2000)]
plt.scatter( df1["Sales"] , df1["Profit"],
            color = "purple",
            marker = "o",
            s=10,
            label = "Sales per profit")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.title("Sales v/s Profit relation")
plt.legend()
plt.xticks()
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

plt.scatter( df["Discount"] , df["Profit"],
            color = "blue",
            marker = "o",
            s=10,
            label = "Sales per profit")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.title("Discount v/s Profit relation")
plt.legend()
plt.xticks()
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

# 5. Histogram
plt.hist( df["Sales"],
         bins=50,
         color = "skyblue",
         edgecolor = "black",
         alpha = 0.7,
         label="Sales Distribution"
         )
plt.xlabel("Sales Range")
plt.ylabel("Sales")
plt.title("Sales Distribution")
plt.legend()
plt.xlim(0,2000)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

plt.hist( df["Profit"],
         bins=50,
         color = "gold",
         edgecolor = "black",
         alpha = 0.7,
         label="Sales Distribution"
         )
plt.xlabel("Profit Range")
plt.ylabel("Profit")
plt.title("Profit Distribution")
plt.legend()
plt.xlim(0,2000)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

plt.hist( df["ShippingCost"],
         bins=30,
         color = "lightgreen",
         edgecolor = "black",
         alpha = 0.7,
         label="ShippingCost Distribution"
         )
plt.xlabel("ShippingCost Range")
plt.ylabel("ShippingCost")
plt.title("ShippingCost Distribution")
plt.legend()
plt.xlim(0,1000)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()

#6. Stacked Bar Graph
category_region_sales = df.groupby(["Category" , "Region"])["Sales"].sum().round(0).reset_index()
# Pivot so Regions become columns
pivot_data = category_region_sales.pivot(index="Category", columns="Region", values="Sales").fillna(0)
# Plot stacked bar chart
colors = ['Crimson', 'Aqua' , 'Olive' , 'Gold' , 'blue' , 'pink' , 'Teal' , 'Navy' , 'Violet' , 'Indigo' , 'Cyan' , 'Magenta' , 'skyblue' ]
pivot_data.plot(kind="bar", stacked=True, figsize=(10,6),
                color= colors[ : len(category_region_sales)],
                edgecolor="black", linewidth=0.5, alpha=0.9)

plt.xlabel("Category-Region")
plt.ylabel("Sales")
plt.title("Category-Region wise sales")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True , linestyle = "-" , color = "grey" , alpha = 0.3 , linewidth = 0.5)
plt.show()
        