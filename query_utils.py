import urllib, json
import media

popular_api = 'https://api.themoviedb.org/3/movie/popular?'
top_rated_api = 'https://api.themoviedb.org/3/movie/top_rated?'

apiKey = '7005d6ab7a4bd1673e2383b5bd8f3d22'
language='en-US'
page='1'
params = urllib.urlencode({'api_key':apiKey, 'language':language, 'page':page })

# Extract the official movie trailer's youtube video id using youtube API
def get_trailer_youtube_id(movie_title):
    youtube_api = 'https://www.googleapis.com/youtube/v3/search?'
    part = 'snippet'
    type = 'video'
    q = movie_title + '+trailer'
    maxResults = '1'
    key = 'AIzaSyB4ZqtNDg2IOGwBsnT4PtBcrB0Xwjm05Qw'
    params = urllib.urlencode({'part':part, 'type':type, 'q':q, 'maxResults':maxResults, 'key':key})

    u = urllib.urlopen(youtube_api + params)
    u_json = json.loads(u.read())

    video_id = u_json['items'][0]['id']['videoId']
    return video_id
    
# Extract related movie information using TMDB API
def extractFeatureFromJson(json):
    list = []
    for i in range(0,20):
        movie_title = (json['results'][i]['title'])
        movie_storyline =(json['results'][i]['overview'])
        poster_image_url = 'https://image.tmdb.org/t/p/w500{}'.format(json['results'][i]['poster_path'])
        trailer_youtube_id = get_trailer_youtube_id(movie_title)
        vote_average = (json['results'][i]['vote_average'])
        popularity = (json['results'][i]['popularity'])
        list.append(media.Movie(movie_title, movie_storyline, poster_image_url, trailer_youtube_id, vote_average, popularity))
    return list
    
# Create the popular movie list
def popular_movie_list():
    u = urllib.urlopen(popular_api, params)
    u_json = json.loads(u.read())
    list = extractFeatureFromJson(u_json)
    return list
    
# Create the top rated movie list
def top_rated_movie_list():
    u = urllib.urlopen(top_rated_api, params)
    u_json = json.loads(u.read())
    list = extractFeatureFromJson(u_json)
    return list


