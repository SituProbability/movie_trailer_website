import webbrowser

class Movie():
    """This class provides a way to store movie related information."""
        
    def __init__(self, movie_title, movie_storyline, poster_image_url, trailer_youtube_id, vote_average, popularity ):
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image_url
        self.trailer_youtube_id = trailer_youtube_id
        self.vote_average = vote_average
        self.popularity = popularity
        
    def display(self):
        print self.title, self.storyline, self.poster_image_url, self.trailer_youtube_id, self.vote_average, self.popularity 
        
