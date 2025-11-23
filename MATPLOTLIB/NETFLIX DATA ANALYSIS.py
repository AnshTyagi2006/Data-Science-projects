import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("MATPLOTLIB/NETFLIX_DATA.csv")


df.drop_duplicates()

df.fillna("Unknown" , inplace=True)
df["date_added"] = pd.to_datetime(df["date_added"] , format='mixed' , dayfirst=True , errors='coerce' )
df.interpolate(method='linear',inplace=True)
year_month = {
    "year" : df["date_added"].dt.year,
    "month" : df["date_added"].dt.month
}
df1=pd.DataFrame(year_month)
print(f"\nYear and month : \n{df1.head(5)}")
print(df.head(5))
#1.
print(f"\nNo. of TV shows v/s Movies : \n",df["type"].value_counts())
#2.
release = df["release_year"].value_counts()
maxrelease = release.idxmax()
print(f"\n{maxrelease} has the highest release of {release.max()}")
#3.
contries = df["country"].value_counts()
maxcontry = contries.head(10)
print(f"\nTop 10 contries producing netflix content : \n{maxcontry}")
#4.
directors = df["director"].value_counts()
maxdirectors = directors.head(10)
print(f"\nTop 10 directors with most titles : \n{maxdirectors}")
#5.
actors = df["cast"].value_counts()
maxactors = actors.head(10)
print(f"\nTop 10 actors who appear the most  : \n{maxactors}")
#6.
genres = df["listed_in"].value_counts()
print(f"\nTop 5 genres are : \n{genres.head(5)}")
#7.

titles = df.groupby("release_year")["title"].count()
print(f"\nTitles added each year : \n{titles}")

# Pre-calculations
# 1. Type counts (Movies vs TV Shows)
type_count = df["type"].value_counts()

# 2. Titles added per year
titles = df.groupby("release_year")["title"].count()

# 3. Top 10 Genres
genres = df["listed_in"].dropna().str.split(", ").explode().value_counts().head(10)

# 4. Top 10 Countries
countries = df["country"].dropna().str.split(", ").explode().value_counts().head(10)

# 5. Top 10 Actors
actors = df["cast"].dropna().str.split(", ").explode().value_counts().head(10)

# 6. Top 10 Directors
directors = df["director"].dropna().str.split(", ").explode().value_counts().head(10)

# 7. Movie Durations (handle Unknowns safely)
movies = df[df["type"] == "Movie"].copy()
movies["minutes"] = (
    movies["duration"].str.replace(" min", "", regex=False)   # remove " min"
)
movies["minutes"] = pd.to_numeric(movies["minutes"], errors="coerce")  # convert safely

# ========================
# PLOTTING (3x3 subplots)
# ========================

fig, ax = plt.subplots(3, 3, figsize=(18, 15))

# 1. Movies vs TV Shows
ax[0,0].bar(type_count.index, type_count.values,
            color=["#063AF5", "#F7600F"], alpha=0.9)
ax[0,0].set_title("Production of Movies & TV Shows")
ax[0,0].set_xlabel("Type")
ax[0,0].set_ylabel("Count")
ax[0,0].grid(True, color="grey", linestyle=":", alpha=0.5)

# 2. Titles added each year
ax[0,1].plot(titles.index, titles.values,
             color="#5107AC", marker="o", linewidth=1)
ax[0,1].set_title("Titles Added Each Year")
ax[0,1].set_xlabel("Release Year")
ax[0,1].set_ylabel("No. of Titles")
ax[0,1].grid(True, color="grey", linestyle=":", alpha=0.5)

# 3. Top 10 Genres
ax[0,2].bar(genres.index, genres.values,
            color="#FD08C8", alpha=0.9)
ax[0,2].set_title("Top 10 Genres")
ax[0,2].set_xlabel("Category")
ax[0,2].set_ylabel("Count")
ax[0,2].tick_params(axis="x", rotation=45)
ax[0,2].grid(True, color="grey", linestyle=":", alpha=0.5)

# 4. Top 10 Countries
ax[1,0].bar(countries.index, countries.values,
            color="#16A34A", alpha=0.9)
ax[1,0].set_title("Top 10 Countries with Most Content")
ax[1,0].set_xlabel("Country")
ax[1,0].set_ylabel("Count")
ax[1,0].tick_params(axis="x", rotation=45)
ax[1,0].grid(True, color="grey", linestyle=":", alpha=0.5)

# 5. Top 10 Actors
ax[1,1].bar(actors.index, actors.values,
            color="#FF7F0E", alpha=0.9)
ax[1,1].set_title("Top 10 Actors on Netflix")
ax[1,1].set_xlabel("Actor")
ax[1,1].set_ylabel("Count")
ax[1,1].tick_params(axis="x", rotation=45)
ax[1,1].grid(True, color="grey", linestyle=":", alpha=0.5)

# 6. Top 10 Directors
ax[1,2].bar(directors.index, directors.values,
            color="#800080", alpha=0.9)
ax[1,2].set_title("Top 10 Directors on Netflix")
ax[1,2].set_xlabel("Director")
ax[1,2].set_ylabel("Count")
ax[1,2].tick_params(axis="x", rotation=45)
ax[1,2].grid(True, color="grey", linestyle=":", alpha=0.5)

# 7. Histogram of Movie Durations
ax[2,0].hist(movies["minutes"].dropna(), bins=30,
             color="red", alpha=0.7)
ax[2,0].set_title("Distribution of Movie Durations")
ax[2,0].set_xlabel("Duration (minutes)")
ax[2,0].set_ylabel("Number of Movies")
ax[2,0].grid(True, color="grey", linestyle=":", alpha=0.5)

# 8. Pie Chart of Movies vs TV Shows
ax[2,1].pie(type_count.values,
            labels=type_count.index,
            autopct="%1.1f%%",
            colors=["#66b3ff", "#ff9999"],
            startangle=90)
ax[2,1].set_title("Share of Movies vs TV Shows")

# 9. Placeholder for new plot
ax[2,2].axis("off")
ax[2,2].text(0.5, 0.5, "(Add another plot here)",
             ha="center", va="center", fontsize=12, color="gray")

plt.tight_layout()
plt.show()




