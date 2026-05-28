```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# PAGE TITLE

st.title("United States Top 50 Playlist Performance Analysis")

# LOAD DATASET

df = pd.read_csv("Atlantic_United_States.csv")

# DATA CLEANING

df['date'] = pd.to_datetime(df['date'], dayfirst=True)

df = df.drop_duplicates()

df = df[
    (df['position'] >= 1) &
    (df['position'] <= 50)
]

df['duration_min'] = df['duration_ms'] / 60000

# DATA OVERVIEW

st.header("Dataset Preview")

st.dataframe(df.head())

st.write("Dataset Shape:", df.shape)

# FEATURE ENGINEERING

days_chart = (
    df.groupby('song')['date']
    .nunique()
    .reset_index(name='days_on_chart')
)

avg_rank = (
    df.groupby('song')['position']
    .mean()
    .reset_index(name='average_rank')
)

best_rank = (
    df.groupby('song')['position']
    .min()
    .reset_index(name='best_rank')
)

volatility = (
    df.groupby('song')['position']
    .std()
    .reset_index(name='rank_volatility')
)

df['popularity_trend'] = (
    df.groupby('song')['popularity']
    .transform(
        lambda x: x.rolling(7, min_periods=1).mean()
    )
)

# POPULARITY DISTRIBUTION

st.header("Popularity Distribution")

fig1, ax1 = plt.subplots(figsize=(10,5))

sns.histplot(
    df['popularity'],
    bins=20,
    kde=True,
    ax=ax1
)

ax1.set_title("Popularity Distribution")
ax1.set_xlabel("Popularity")
ax1.set_ylabel("Frequency")

st.pyplot(fig1)

st.markdown("""
The histogram of popularity scores shows a highly concentrated distribution between popularity scores of 80 and 100, indicating that most songs appearing in the United States Top 50 playlist already possess high popularity levels.

The majority of observations cluster toward higher popularity values with relatively fewer low-popularity songs.
""")

# POPULARITY VS RANK

st.header("Popularity vs Playlist Rank")

fig2, ax2 = plt.subplots(figsize=(10,6))

sns.scatterplot(
    x='popularity',
    y='position',
    data=df,
    ax=ax2
)

ax2.invert_yaxis()

ax2.set_title("Popularity vs Rank")
ax2.set_xlabel("Popularity")
ax2.set_ylabel("Playlist Rank")

st.pyplot(fig2)

st.markdown("""
The scatter plot between popularity and playlist rank demonstrates a moderate inverse relationship between the two variables.

Songs with higher popularity scores tend to occupy better playlist positions.

The observed pattern suggests a negative correlation because lower numerical ranks correspond to better playlist positions.
""")

# EXPLICIT VS NON-EXPLICIT

st.header("Explicit vs Non-Explicit Song Performance")

fig3, ax3 = plt.subplots(figsize=(8,5))

sns.boxplot(
    x='is_explicit',
    y='popularity',
    data=df,
    ax=ax3
)

ax3.set_title("Explicit vs Non-Explicit Popularity")

st.pyplot(fig3)

st.markdown("""
The boxplot comparison between explicit and non-explicit songs indicates that both categories exhibit highly similar popularity distributions.

Median popularity scores are nearly identical, and the interquartile ranges substantially overlap.

Both distributions contain several lower-popularity outliers, indicating occasional poor-performing tracks in both content categories.

However, there is no strong statistical evidence suggesting that explicit content significantly increases or decreases popularity.
""")

# ARTIST DOMINANCE

st.header("Top 10 Artists by Playlist Appearances")

artist_counts = (
    df['artist']
    .value_counts()
    .head(10)
)

fig4, ax4 = plt.subplots(figsize=(12,6))

sns.barplot(
    x=artist_counts.values,
    y=artist_counts.index,
    ax=ax4
)

ax4.set_title("Top 10 Artists by Playlist Appearances")

st.pyplot(fig4)

st.markdown("""
The artist dominance analysis reveals substantial inequality in playlist representation among artists.

Taylor Swift, Zach Bryan, and Morgan Wallen exhibit significantly higher playlist appearances compared to other artists, indicating strong market concentration.

The large differences between artists indicate non-uniform representation across the playlist ecosystem.
""")

# SONG RANK TREND

st.header("Song Rank Trend")

top_song = (
    df['song']
    .value_counts()
    .index[0]
)

song_df = df[
    df['song'] == top_song
]

fig5, ax5 = plt.subplots(figsize=(12,6))

ax5.plot(
    song_df['date'],
    song_df['position']
)

ax5.invert_yaxis()

ax5.set_title(f"Rank Trend: {top_song}")

st.pyplot(fig5)

st.markdown("""
The time-series plot of playlist rank demonstrates substantial rank fluctuations over time, indicating dynamic playlist movement behavior.

The song exhibits both upward and downward rank transitions, suggesting varying listener engagement intensity throughout the observation period.
""")

# CORRELATION MATRIX

st.header("Correlation Matrix")

correlation_data = df[[
    'position',
    'popularity',
    'duration_ms',
    'total_tracks',
    'duration_min'
]]

correlation_matrix = correlation_data.corr()

fig6, ax6 = plt.subplots(figsize=(8,6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='coolwarm',
    ax=ax6
)

ax6.set_title("Correlation Matrix")

st.pyplot(fig6)

st.markdown("""
Position vs Popularity:
A weak negative correlation exists between playlist position and popularity.

Position vs Total Tracks:
A weak positive relationship exists between playlist position and album size.

Popularity vs Total Tracks:
A weak negative relationship exists between popularity and album track count.

Popularity vs Duration:
The relationship between song duration and popularity is extremely weak.

Duration_ms vs Duration_min:
A perfect positive correlation exists because duration in minutes is directly derived from duration in milliseconds.

Overall Conclusion:
The heatmap reveals that most variables exhibit weak correlations. Playlist behavior is influenced by multiple interacting factors rather than a single dominant variable.
""")

# FINAL CONCLUSION

st.header("Overall Research Conclusion")

st.markdown("""
1. Most songs in the Top 50 playlist possess very high popularity scores.

2. Playlist rankings demonstrate highly dynamic movement behavior.

3. Songs with longer chart duration and lower volatility exhibit sustainable listener engagement.

4. Taylor Swift, Zach Bryan, and Morgan Wallen dominate playlist appearances.

5. Higher popularity generally improves ranking performance.

6. Explicit and non-explicit songs exhibit similar popularity distributions.

7. Song duration and album size exhibit weak influence on playlist success.

Final Research Conclusion:

The United States Top 50 playlist ecosystem is highly dynamic, competitive, and engagement-driven.

Playlist success depends on sustained listener retention, chart stability, artist dominance, and long-term engagement persistence.

Streaming-era music analytics requires multidimensional evaluation rather than reliance on isolated popularity metrics alone.
""")
```













