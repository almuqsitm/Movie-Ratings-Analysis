import streamlit as st
import pandas as pd
import plotly.express as px

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Movie Lens Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_data():
    df = pd.read_csv("data/movie_ratings.csv")  # Replace with your file path
    return df


def plot_genre_counts(df):
    """Creates a horizontal bar chart of the number of ratings per genre."""
    genre_counts = df["genres"].value_counts().reset_index()
    genre_counts.columns = ["genres", "count"]

    fig = px.bar(
        genre_counts,
        x="count",
        y="genres",
        orientation="h",
        color="count",
        color_continuous_scale="Plasma",
        title="Number of Ratings per Genre",
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"},
        title_font_size=20,
        font=dict(color="white"),
        xaxis=dict(
            showgrid=True,
            gridcolor="gray",
            gridwidth=1,
            griddash="dot",  # makes the vertical lines dotted
        ),
    )

    return fig


def plot_5star_treemap(df):
    """Creates a treemap showing the distribution of 5-star ratings per genre."""
    # Filter for 5-star ratings
    top_ratings = df[df["rating"] == 5].reset_index(drop=True)

    # Count number of 5-star ratings per genre
    genre_counts = top_ratings["genres"].value_counts().reset_index()
    genre_counts.columns = ["genres", "count"]

    # Create treemap
    fig = px.treemap(
        genre_counts,
        path=["genres"],  # hierarchy: just genre
        values="count",  # size of each rectangle = number of 5-star ratings
        color="count",  # color by number of 5-star ratings
        color_continuous_scale="Plasma",  # bright for dark background
        title="5-Star Ratings Distribution Across Genres",
    )

    # Dark background
    fig.update_layout(template="plotly_dark", font=dict(color="white"))

    return fig


def plot_mean_rating_by_year(df):
    """Creates a line chart showing mean movie rating by release year."""
    # Aggregate: mean rating per movie release year
    mean_ratings = df.groupby("year")["rating"].mean().reset_index()

    fig = px.line(
        mean_ratings,
        x="year",
        y="rating",
        title="Mean Movie Rating by Release Year",
        markers=True,  # show dots for each year
    )

    # Dark theme
    fig.update_layout(template="plotly_dark", font=dict(color="white"))

    return fig


def top_movies_table(df, min_ratings=50, top_n=5):
    """Returns the top N movies with at least min_ratings."""
    movie_stats = (
        df.groupby("title")
        .agg(avg_rating=("rating", "mean"), rating_count=("rating", "count"))
        .reset_index()
    )

    # Filter for minimum number of ratings
    filtered_movies = movie_stats[movie_stats["rating_count"] >= min_ratings]

    # Sort by average rating descending
    top_movies = filtered_movies.sort_values("avg_rating", ascending=False).head(top_n)

    return top_movies


def main():
    # Header
    st.title("🎬 Movie Lens Analytics Dashboard")
    st.markdown("---")

    # Load dataframe
    df = load_data()

    # # Display dataframe
    # st.subheader("Movie Ratings Dataset")
    # st.dataframe(df)
    # q1
    st.subheader("What's the breakdown of genres for the movies that were rated?")
    fig = plot_genre_counts(df)
    st.plotly_chart(fig, use_container_width=True)

    # q2
    st.subheader("Which genres have the highest viewer satisfaction (highest ratings)?")
    treemap_fig = plot_5star_treemap(df)
    st.plotly_chart(treemap_fig, use_container_width=True)

    # q3
    st.subheader("How does mean rating change across movie release years?")
    rating_trend_fig = plot_mean_rating_by_year(df)
    st.plotly_chart(rating_trend_fig, use_container_width=True)

    # q4
    st.subheader("Top Movies with at Least 50 Ratings")
    top_50_movies = top_movies_table(df, min_ratings=50, top_n=5)
    top_50_movies = top_50_movies.reset_index(drop=True)

    st.dataframe(top_50_movies)

    st.subheader("Top Movies with at Least 150 Ratings")
    top_150_movies = top_movies_table(df, min_ratings=150, top_n=5)
    top_150_movies = top_150_movies.reset_index(drop=True)

    st.dataframe(top_150_movies)


if __name__ == "__main__":
    main()
