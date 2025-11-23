import pandas as pd
import numpy as np
import random

#    OrderID CustomerName   Gender     Product     Category  OrderDate  Quantity  PricePerUnit  Discount% PaymentMode       City  Expected Amount  TotalAmount
# 0    O1000       Carlos    Other     Unknown      Unknown 2023-09-06      10.0       10000.0        5.0        Cash    Unknown         100000.0     95000.00
# 1    O1001         Sara   Female      Mobile      Grocery 2023-06-15       5.0      167203.0       26.0        Cash  Bangalore         836015.0    618651.10
# 2    O1002      Unknown   Female     Unknown      Unknown 2023-12-01      10.0       10000.0        0.0      Wallet     Delhii         100000.0    100000.00
# 3    O1003       Fatima  Unknown  Headphones  Electronics 2023-01-30       3.0      167203.0       26.0         UPI    Unknown         501609.0    371190.66
# 4    O1004          Ali   Female  Headphones      Unknown 2023-09-04       3.0      167203.0       50.0         UPI    Chennai         501609.0    250804.50
# 5    O1005       Carlos  Unknown     Unknown      Unknown 2023-04-16       1.0        1500.0       10.0        Cash    Unknown           1500.0      1350.00
# 6    O1006      Unknown    Other      Laptop     Clothing 2023-02-20      50.0         500.0       30.0         UPI     Mumbai          25000.0     17500.00
# 7    O1007         Ravi    Other     Unknown     Clothing 2023-03-22       2.0        3000.0       50.0        Cash      Delhi           6000.0      3000.00
# 8    O1008       Carlos     Male       Mixer     Clothing 2023-05-13       2.0        2250.0       10.0        Card    Chennai           4500.0      4050.00
# 9    O1009      Unknown   Female       Mixer      Unknown 2023-10-12       2.0        1500.0       20.0        Cash     Delhii           3000.0      2400.00
# 10   O1010      Unknown  Unknown      Laptop         Home 2023-05-18      10.0         500.0       50.0      Wallet     Delhii           5000.0      2500.00
# 11   O1011       Fatima   Female     Unknown      Unknown 2023-07-03      10.0      167203.0       20.0         UPI     Mumbai        1672030.0   1337624.00
# 12   O1012          Ali    Other       Mixer         Home 2023-11-26       2.0        2500.0        5.0        Card     Mumbai           5000.0      4750.00
# 13   O1013         Sara     Male     Unknown         Home 2023-09-30       5.0       10000.0        5.0        Cash    Chennai          50000.0     47500.00
# 14   O1014       Fatima     Male     Unknown     Clothing 2023-12-06       2.0      167203.0        0.0         UPI    Unknown         334406.0    334406.00

#reading file
df = pd.read_excel("PANDAS/Ecommerce_Orders_Data.xlsx")
#datatype of orderdate
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
# filling missing numbers
df.interpolate(method="linear" , inplace=True)
#filling missing items
df[["CustomerName" , "Product" , "Category" , "City"]] = df[["CustomerName" , "Product" , "Category" , "City"]].fillna("Unknown")
df.loc[( df["City"] == "Delhii" ), "City"] = "Delhi"
df["Gender"] = df["Gender"].fillna(random.choice(["Male" , "Female" , "Other"]))
df["PaymentMode"] = df["PaymentMode"].fillna(random.choice(["Cash" , "Card" , "UPI" , "Wallet"]))
#Cleaning the data
df.loc[df["Quantity"]<0 , "Quantity"] = df["Quantity"].mean().round(0)
df.loc[ df["PricePerUnit"] < 0  , "PricePerUnit"] = df["PricePerUnit"].mean().round(0)
df.loc[ (df["PricePerUnit"]>100000.0) | (df["PricePerUnit"]<0.0) , "PricePerUnit"] = df["PricePerUnit"].mean().round(0)
df.loc[ (df["Discount%"]<0.0) | (df["Discount%"]>100.0) , "Discount%"] = df["Discount%"].mean().round(0)
df["TotalAmount"] = (df["Quantity"] * df["PricePerUnit"]) * (1 - (df["Discount%"]/100) ) 
# adding a coulmn
df.insert(11 , "Expected Amount" ,  (df["Quantity"] * df["PricePerUnit"]) )
#removing large ammountsExpected
largeamm = df["TotalAmount"].mean() + (df["TotalAmount"].std() * 3)
df.loc[ df["TotalAmount"] > largeamm , "TotalAmount"] = None
df.dropna()
#saving the file
df.to_excel("Cleaned_Ecommerce_Orders_Data.xlsx"  , index=False)
print(" Succesfully saved your file : 'Cleaned_Ecommerce_Orders_Data.xlsx' ✅")

#extracting day and month from orderdate
print( f"The days and months of the orders are : \n{df['OrderDate'].dt.day }\n{df['OrderDate'].dt.month}")

#Data Analysis
revenue = df["Expected Amount"].max()
max_revenue = df.loc[ df["Expected Amount"] == df["Expected Amount"].max() , "City"].iloc[0]
print(f"\n{max_revenue} city has the highest revenue  of  {revenue} . ")

order = df["Quantity"].max()
max_order = df.loc[ df["Quantity"]  == order , "Product"].iloc[0]
print(f"\n{max_order} has the highest order of {order} . ")

print(f"\nTop 5 products are : \n")
top_5prod = df.groupby("Product")["Expected Amount"].sum().nlargest(5)
print(top_5prod)

order_paymode = df.groupby("PaymentMode")["Expected Amount"].mean().round()
print(f"The average order value for all payment modes are :\n{order_paymode} ")

months = np.array(df["OrderDate"].dt.month)
print(f"\nTotal orders per month are :\n")
order_permonth = df.groupby(df["OrderDate"].dt.month)["Quantity"].sum()
print(order_permonth)

high_quantity =df[df["Quantity"]>50]
if not high_quantity.empty:
    print(f"\nCustomers with unusual high quantites are : {high_quantity}\n")
else:
    print("\nNo customers with unusual high quantities(>50) found")    

#grouping


category_stats = df.groupby("Category").agg({
    "Expected Amount": "sum",
    "Discount%": "mean",
    "Quantity": "sum"
}).round(0)

print("\nCategory-wise summary:\n")
print(category_stats)


gender = df.loc[df["Expected Amount"] == df["Expected Amount"].max() , "Gender"].max()
purchase_pattern = df.groupby(["City" , "Gender"])["Expected Amount"].max()
print(purchase_pattern)

comon_paymode = df.loc[df["PaymentMode"] == df["PaymentMode"].count().sum() , "City"]
print(comon_paymode)
