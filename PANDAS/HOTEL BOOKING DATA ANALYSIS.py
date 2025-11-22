import pandas as pd
import random

#    BookingID CustomerName  Gender CheckInDate  Nights  RoomType  PricePerNight  Discount%       City PaymentMode    TotalAmount
# 0      B1000        Priya    Male  2023-05-29     6.0     Suite         1000.0       32.0     Mumbai      Wallet           6000.0       4080.0
# 1      B1001       Fatima    Male  2023-08-22     3.0     Suite         5000.0       32.0  Bangalore         UPI          15000.0      10200.0
# 2      B1002      Unknown  Female  2023-04-21    10.0     Suite         1000.0       32.0     Mumbai         UPI          10000.0       6800.0
# 3      B1003          Ali  Female  2023-08-29     3.0     Suite        20000.0       32.0      Delhi        Cash          60000.0      40800.0
# 4      B1004        Sarah    Male  2023-11-12     4.0  Standard       101377.0       20.0      Delhi      Wallet         405508.0     324406.0
# 5      B1005       Carlos    Male  2023-06-13    10.0    Deluxe       101377.0       32.0      Delhi      Wallet        1013770.0     689364.0
# 6      B1006        Priya    Male  2024-01-06     6.0     Suite        20000.0       20.0  Bangalore      Wallet         120000.0      96000.0
# 7      B1007        Sarah    Male  2023-06-21     2.0     Suite       101377.0        5.0      Delhi         UPI         202754.0     192616.0
# 8      B1008        Priya   Other  2023-12-11     8.0    Deluxe       101377.0        0.0  Bangalore      Wallet         811016.0     811016.0
# 9      B1009          Ali    Male  2023-06-06     6.0    Deluxe        20000.0       50.0  Bangalore      Wallet         120000.0      60000.0
# 10     B1010        Priya   Other  2023-07-21     4.0     Suite         1000.0        5.0    Chennai      Wallet           4000.0       3800.0
# 11     B1011        Sarah  Female  2023-04-14     9.0  Standard       101377.0       32.0     Mumbai      Wallet         912393.0     620427.0
# 12     B1012          Ali  Female  2024-01-30     6.0     Suite       101377.0       32.0    Chennai      Wallet         608262.0     413618.0
# 13     B1013        Priya    Male  2024-01-01     2.0     Suite       101377.0       32.0     Mumbai      Wallet         202754.0     137873.0
# 14     B1014      Unknown    Male  2023-01-05     3.0     Suite       101377.0       10.0     Mumbai      Wallet         304131.0     273718.0

#reading file
df = pd.read_excel("Healthcare_Patient_Data.xlsx")
#datatype of date
df["CheckInDate"] = pd.to_datetime(df["CheckInDate"] , format='mixed' , dayfirst=True , errors="coerce")
#missing numeric values
df.interpolate(method="linear" ,  inplace=True)
df.loc[ df["Nights"]<0 , "Nights"] = df["Nights"].median().round()
df.loc[ (df["PricePerNight"] < 0) | (df["PricePerNight"] > 50000), "PricePerNight"] = df["PricePerNight"].mean().round()
df.loc[ (df["Discount%"] < 0) | (df["Discount%"] > 100) | (df["Discount%"].isnull() == True) , "Discount%" ] = df["Discount%"].mean().round()
df.insert(column="ExpectedAmount" ,  loc=10 , value= (df["PricePerNight"] * df["Nights"])) #adding new column
df["TotalAmount"] = (df["Nights"] * df["PricePerNight"]  * (1 - (df["Discount%"]/100) ) ).round()
#missing items
df["CustomerName"] = df["CustomerName"].fillna("Unknown")
df.loc[ (df["Gender"] == "Unknown") | (df["Gender"] == "nan") | (df["Gender"].isnull() == True), "Gender"] = random.choice(['Female', 'Male' ,'Other'])
df.loc[ (df["RoomType"] == "Unknown") | (df["RoomType"] == "nan") | (df["RoomType"].isnull() == True), "RoomType"] = random.choice(['Suite', 'Standard', 'Deluxe'])
df.loc[ df["City"] == "Mumbay" , "City"] = "Mumbai"
df.loc[ df["City"] == "Banglore" , "City"] = "Bangalore"
df.loc[ (df["City"] == "Unknown") | (df["City"] == "nan") | (df["City"].isnull() == True) , "City"] = random.choice(['Mumbai', 'Banglore' ,'Chennai', 'Delhi'])
df.loc[ (df["PaymentMode"] == "Unknown") | (df["PaymentMode"] == "nan") | (df["PaymentMode"].isnull() == True), "PaymentMode"] = random.choice(['Wallet', 'UPI' ,'Cash' ,'Card'])
#saving file
df.to_excel("Cleaned_Hotel_Bookings_Data.xlsx", index=False)
print( "\nFILE SAVED SUCCESFULLY : Cleaned_Hotel_Bookings_Data.xlsx ✅\n")
#printing the data
print(df.head(15))

#feature engineering
checkin ={
    "day" : (df["CheckInDate"].dt.day),
    "month" : (df["CheckInDate"].dt.month)
}
df1 = pd.DataFrame( checkin )
print(f"\nThe checkin days are : \n{df1.head(15)}")
# highamm = df["TotalAmount"].mean() + (3 * df["TotalAmount"].std())
# lowamm = df["TotalAmount"].mean() - (3 * df["TotalAmount"].std())
# df = df[(df["TotalAmount"]<highamm) & (df["TotalAmount"] > lowamm)]
# print(f"\nThe Total Ammount within the outliers are : \n{df.head()}")

#Data analysis
city_revenue = df.groupby("City")["ExpectedAmount"].sum()
max_city = city_revenue.idxmax()
max_city_value = city_revenue.max()
print(f"\nCity with highest total revenue: {max_city} ({max_city_value})")

# 2. Room type with highest total bookings (sum of nights)
room_bookings = df.groupby("RoomType")["Nights"].sum()
top_room = room_bookings.idxmax()
top_room_value = room_bookings.max()
print(f"\nRoom type with highest total nights booked: {top_room} ({top_room_value} nights)")

# 3. Customer with highest total spent
customer_spent = df.groupby("CustomerName")["TotalAmount"].sum()
top_customer = customer_spent.idxmax()
top_customer_value = customer_spent.max()
print(f"\nCustomer with highest total spend: {top_customer} ({top_customer_value})")

# 4. Average booking value by payment mode
avg_payment = df.groupby("PaymentMode")["TotalAmount"].mean().round()
print(f"\nAverage booking value per payment mode:\n{avg_payment}")

# 5. Total booking amount per month
monthly_booking = df.groupby(df["CheckInDate"].dt.month)["TotalAmount"].sum().round()
print(f"\nTotal booking amount per month:\n{monthly_booking}")

# 6. Bookings with unusually high nights (>10)
high_nights = df[df["Nights"] > 10]
if not high_nights.empty:
    print(f"\nBookings with unusually high nights (>10):\n{high_nights}")
else:
    print("\nNo bookings with unusually high nights (>10) found")

# 7. Room type wise aggregated details
room_summary = df.groupby("RoomType").agg({
    "ExpectedAmount": "sum",
    "Discount%": "mean",
    "Nights": "sum"
}).round()
print(f"\nRoom type wise booking summary:\n{room_summary}")

# 8. Gender with highest total booking amount (overall, not city-wise)
gender_total = df.groupby("Gender")["TotalAmount"].sum()
top_gender = gender_total.idxmax()
top_gender_value = gender_total.max()
print(f"\nGender with highest total booking amount: {top_gender} ({top_gender_value})")

# 9. Most common payment mode
common_payment = df["PaymentMode"].mode()[0]
print(f"\nMost common payment mode: {common_payment}")
