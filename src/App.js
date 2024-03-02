// app.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [topMovies, setTopMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [searchedUsername, setSearchedUsername] = useState('');
  const [totalMovies, setTotalMovies] = useState(0);
  const [totalRates, setTotalRates] = useState(0);
  const [error, setError] = useState('');

  const handleGetTopMovies = async () => {
    try {
      setLoading(true);
      setTopMovies([]); // Reset topMovies array
      setSearched(false); // Hide profile when clicking the button
      setError('');
      const response = await axios.post('http://localhost:5000/get_top_movies', { username });
      const { top_movies, totalR, totalM } = response.data;

      // Show only 4 movies
      const maxMoviesToShow = 4;
      let moviesToShow = top_movies.slice(0, maxMoviesToShow);

      // Randomize if the user has more than 4 max rated movies
      if (totalR > maxMoviesToShow) {
        moviesToShow = moviesToShow.sort(() => Math.random() - 0.5);
      }

      setTopMovies(moviesToShow);
      setSearched(true);
      setSearchedUsername(username);
      setTotalMovies(totalM);
      setTotalRates(totalR);
      if (totalR < 10) {
        setError('User does not have at least 10 rated movies.');
        setTopMovies([]);
      }
    } catch (error) {
      console.error('Error getting top movies:', error);
      setTopMovies([]);
      setSearched(false);
      setError('User not found or has no movies on the account.');
    } finally {
      setLoading(false);
    }
  };

  const handleRedirect = (url) => {
    window.open(url, '_blank');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleGetTopMovies();
    }
  };

  const handleDataAnalysis = () => {
    window.location.href = '/analysis.html';
  };
  

  return (
    <div className="App">
      <h1>Your Random Letterboxd Top 4</h1>
      <div className="labelContainer">
        <label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyPress={handleKeyPress}
            className="searchBox"
            placeholder="Letterboxd Username"
          />
        </label>
        <button
          onClick={handleGetTopMovies}
          className="getTopMoviesBtn"
          disabled={loading || !username}
        >
          Get Top Movies
        </button>
      </div>

      {searched && !loading && totalMovies > 0 && (
        <div
          className="userProfileContainer"
          onClick={() => window.open(`https://letterboxd.com/${searchedUsername}`, '_blank')}
        >
          <img className="userProfileImage" src="prof.png" alt="User Profile" />
          <p className="searchedUsername">
            Account Username: {searchedUsername} ({totalRates} Rated Movies)
          </p>
        </div>
      )}

      {error && <p className="errorText">{error}</p>}

      <div className="loadingContainer" style={{ display: loading ? 'block' : 'none' }}>
        <div className="loadingCircle" />
      </div>

      <div className="topMovies">
        {topMovies.map((movie, index) => (
          <div key={index} className="movieCard">
            <a href={`https://letterboxd.com/film/${movie.slug}`} target="_blank" rel="noopener noreferrer">
              <img
                src={movie.poster}
                alt={movie.title}
              />
            </a>
            <div className="movieDetails">
              <h3>{movie.title}</h3>
              <p>{`Director(s): ${movie.director}`}</p>
              <p>{`Year: ${movie.year}`}</p>
              <p>{`Genres: ${movie.genres}`}</p>
              <p>{`Rating: ${movie.rating}`}</p>
            </div>
          </div>
        ))}
      </div>
      <button
          onClick={handleDataAnalysis}
          className="dataAnalysisBtn"
        >
          Data Analysis
        </button>
    </div>
  );
}

export default App;
