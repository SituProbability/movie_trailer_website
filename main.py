import media
import generate_movie_page
import query_utils

# Generate a popular movie list
popular_movies = query_utils.popular_movie_list()
# Generate a top rated movie list
top_rated_movies = query_utils.top_rated_movie_list()

# Generate the web page
generate_movie_page.open_movies_page(popular_movies, top_rated_movies)

