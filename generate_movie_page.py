import webbrowser
import os
import re


# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
            margin-bottom:30px;
        }
        .navbar-inverse .navbar-header a,
        .navbar-inverse .navbar-nav li a{
            color:#D5D5D5
        }	
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
            border:5px;
	    border-radius: 10px;
	    box-shadow: 5px 5px 20px #ccc;
	    background-color:#e1e1ef;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .media-heading{
	    overflow-y:scroll;
	    max-height:26px;
	}
        blockquote{
            overflow-y:scroll;
            max-height:150px;
	}
        .btn{
            margin-top:10px;
	    margin-bottom:10px
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        footer{
            width:100%;
	    background-color:#333534;
	    padding:5px;
	    color:#FFF;
	}
	@media (min-width:768px){
	    .section{
		display:flex;
		flex-wrap:wrap;
	    }
	}
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>    
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
      <!-- Trailer Video Modal -->
        <div class="modal" id="trailer">
          <div class="modal-dialog">
            <div class="modal-content">
              <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
                <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
              </a>
              <div class="scale-media" id="trailer-video-container">
              </div>
            </div>
          </div>
        </div>

      <!-- Main Page Content -->
      <div class="container">
        {nav_bar}
      </div>

      <div class="container section">
        {movie_tiles}
      </div>

      <footer class="container-fluid text-right footer navbar-fixed-bottom">
        Developed by Gordon Situ. Information courtesy of TMDB,YOUTUBE.
      </footer>
  </body>
</html>
'''
# Navigation bar for most viewed page
most_viewed_nav_bar = '''
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container-fluid">
          <div class="navbar-header">
            <a class="navbar-brand" href="index.html">My Favorite Movie Trailers</a>
			<button type="button" class="navbar-toggle" data-toggle="collapse" 
				data-target="#myNavbar" >
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
			</button>
          </div>
		  <div class="collapse navbar-collapse" id="myNavbar">
			  <ul class="nav navbar-nav">
				<li class="active"><a href="index.html">Most Viewed</a></li>
				<li><a href="top_rated/index.html">Top Rated</a></li>	
			  </ul>
		  </div>
        </div>
      </div>
'''

# Navigation bar for top rated page
top_rated_nav_bar = '''
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container-fluid">
          <div class="navbar-header">
            <a class="navbar-brand" href="../index.html">My Favorite Movie Trailers</a>
			<button type="button" class="navbar-toggle" data-toggle="collapse" 
				data-target="#myNavbar" >
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
			</button>
          </div>
		  <div class="collapse navbar-collapse" id="myNavbar">
			  <ul class="nav navbar-nav">
				<li><a href="../index.html">Most Viewed</a></li>
				<li class="active"><a href="index.html">Top Rated</a></li>	
			  </ul>
		  </div>
        </div>
      </div>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-sm-6 movie-tile" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <div class="media-left">
	<img src="{poster_image_url}" class="media object" style="width:220px;height:315px" >
    </div>		
    <div class="media-body">
	<h3 class="media-heading">{movie_title}</h3>
	<button type="button" class="btn btn-primary">Rating <span class="badge">{vote_average}</span></button>
	<h4 id="overview-header">Overview</h4>
	<blockquote><p>{movie_storyline}</p></blockquote>
	<h4>Popularity: <small class="text-primary">{popularity}</small></h4>
    </div>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        
        # Append the tile for the movie with its content filled in {} {}
        content += movie_tile_content.format(
            movie_title = movie.title,
            poster_image_url = movie.poster_image_url,
            trailer_youtube_id = movie.trailer_youtube_id,
            vote_average = movie.vote_average,
            movie_storyline = movie.storyline.encode('utf-8'),
            popularity = movie.popularity,
        )
    return content

def create_output_file(path, movies, nav_bar):
    # Create or overwrite the output file
    output_file = open(path, 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        nav_bar=nav_bar,
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()
    return output_file
    
def open_movies_page(popular_movies, top_rated_movies):
    # Create a directory for top_rated output
    path = "index.html"
    top_rated_folder = "top_rated"
    if not os.path.exists(top_rated_folder):
        os.makedirs(top_rated_folder)

    top_rated_path = os.path.join(top_rated_folder, path)
    create_output_file(top_rated_path, top_rated_movies, top_rated_nav_bar)

    popular_output_file = create_output_file(path, popular_movies, most_viewed_nav_bar)
    
    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(popular_output_file.name)
    webbrowser.open('file://' + url, new=2)
