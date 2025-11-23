import pandas as pd
import random 

df = pd.read_excel("Healthcare_Patient_Data.xlsx")
#   PatientID     Name  Age  Gender    Diagnosis    Treatment AdmissionDate DischargeDate  BillAmount  Discount%  TotalAmount       City PaymentMode
# 0     P1000    Priya   14  Female      General  Treatment A    2023-05-11    2023-05-13        2681          7      2493.33  Hyderabad        Cash
# 1     P1001    Priya   34  Female   Pediatrics  Treatment B    2023-02-07    2023-02-14        2681          7      2493.33      Delhi        Cash
# 2     P1002    Aarav   35  Female  Orthopedics  Treatment A    2023-08-01    2023-08-04        2681          7      2493.33      Delhi         UPI
# 3     P1003    Rohit   72   Other  Orthopedics  Treatment A    2023-01-08    2023-01-10        2681          5      2546.95      Delhi        Card
# 4     P1004     Sara    6    Male   Pediatrics  Treatment C    2023-04-10    2023-04-17        2681          7      2493.33  Hyderabad        Card
# 5     P1005    Rohit   35   Other   Pediatrics  Treatment C    2023-05-21    2023-05-28        2681          7      2493.33    Chennai        Card
# 6     P1006  UNKNOWN   35  Female      General  Treatment A    2023-01-09    2023-01-19        4820          7      4482.60    Chennai        Cash
# 7     P1007    Rohit   35   Other    Neurology  Treatment A    2023-11-30    2023-12-05        2978          7      2769.54  Hyderabad        Card
# 8     P1008    Priya   35   Other  Orthopedics  Treatment A    2023-12-25    2023-12-26        2681          7      2493.33  Hyderabad        Card
# 9     P1009  UNKNOWN   61  Female   Cardiology  Treatment B    2023-01-31    2023-02-01        2681         17      2225.23  Bangalore        Cash

# 3. Data Analysis
# City with highest total revenue.
# Diagnosis with maximum patients.
# Patient who spent the highest amount.
# Average bill value for each PaymentMode.
# Total revenue per month.
# Identify patients with unusually high bills (e.g., > 50,000).
# Department-wise (Diagnosis) summary: total bill, avg discount, total patients.
# Gender that spent the most amount overall.
# Most common payment mode.
df[["AdmissionDate" , "DischargeDate"]] = df[["AdmissionDate" , "DischargeDate"]].apply(pd.to_datetime)
df[["Age" , "BillAmount" , "Discount%"]] = df[["Age" , "BillAmount" , "Discount%"]].apply(pd.to_numeric)
df.interpolate(method='linear' , inplace=True)
df.loc[( df["Age"] < 0 ) | (df["Age"] >100) | (df["Age"].isnull()==True) , "Age"] = df["Age"].median()
df["Age"] = df["Age"].round(0)
df.loc[( df["BillAmount"] < 0 ) | (df["BillAmount"] >5000) | (df["BillAmount"].isnull()==True) , "BillAmount"] = df["BillAmount"].median()
df["BillAmount"] = df["BillAmount"].round(0)
df.loc[( df["Discount%"] < 0 ) | (df["Discount%"] >100) | (df["Discount%"].isnull()==True) , "Discount%"] = df["Discount%"].median()
df["Discount%"] = df["Discount%"].round(0)

df.loc[( df["Name"] == "nan" ) | (df["Name"].isnull()==True) , "Name"] = "UNKNOWN"
df.loc[( df["Gender"] == "nan" ) | (df["Gender"].isnull()==True) , "Gender"] = random.choice(['Female','Male' ,'Other'])
df.loc[( df["Diagnosis"] == "nan" ) | (df["Diagnosis"].isnull()==True) , "Diagnosis"] = random.choice(['Pediatrics' ,'Orthopedics', 'Neurology' ,'Cardiology', 'General'])
df.loc[( df["Treatment"] == "nan" ) | (df["Treatment"].isnull()==True) , "Treatment"] = random.choice(['Treatment A', 'Treatment B','Treatment C'])
df.loc[df["City"] == "Delhii" , "City"] = "Delhi"
df.loc[( df["PaymentMode"] == "nan" ) | (df["PaymentMode"].isnull()==True) , "PaymentMode"] = random.choice(['Cash' ,'UPI','Card'])
df.insert( 10 , "TotalAmount" , df["BillAmount"] * (1-df["Discount%"]/100))
df.to_excel("Cleaned_Healthcare_Patient_Data.xlsx")
print(df.head(10))

dates = {
    "Date" : df["AdmissionDate"].dt.day,
    "Month" : df["AdmissionDate"].dt.month
}
df1 = pd.DataFrame(dates)
print(f"\nThe admission dates are : \n{df1.head(10)}")

city_revenue = df.groupby("City")["BillAmount"].sum()
city_max_revenue = city_revenue.idxmax(0)
print(f"{city_max_revenue } generates the highest total revenue.")

diag_patient = df.groupby("Diagnosis")["BillAmount"].sum()
diag_max_patient = diag_patient.idxmax(0)
print(f"{diag_max_patient}  diagnosis has the maximum patients.")

patient_amm = df.groupby("Name")["TotalAmount"].sum()
patient_max_amm = patient_amm.idxmax(0)
print(f"{patient_max_amm} has spent the highest amount.")

avg_bill_paymode = df.groupby("PaymentMode")["BillAmount"].mean()
print(f"The average bill amount per payment mode is : \n{avg_bill_paymode}")

revenue_month = df.groupby(df["AdmissionDate"].dt.month)["BillAmount"].sum()
print(f"The total revenue per month is : \n{revenue_month}")

diagnosis_summary = df.groupby("Diagnosis").agg({
    "BillAmount" : "sum",
    "Discount%" : "mean",
    "Treatment" : "count",
})
print(f"Diagnosis Summary : \n{diagnosis_summary}")

gender_amm = df.groupby("Gender")["TotalAmount"].sum()
gender_max_amm = gender_amm.idxmax(0)
print(f"{gender_max_amm} has spent the highest ammount.")

common_paymode = df["PaymentMode"].mode()[0]
print(f"{common_paymode} is the most common payment mode.\n")


