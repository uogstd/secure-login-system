import React, { useEffect, useState, useRef } from 'react';
import { jwtDecode } from 'jwt-decode';
import './App.css';

const API_URL = process.env.REACT_APP_API_URL; // Move this here for modular use

function App() {
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const googleButtonRef = useRef(null);

  function handleCallbackResponse(response) {
    const userObject = jwtDecode(response.credential);
    setUser(userObject);
  }

  function handleSignOut() {
    setUser(null);

    // Clear and re-render the Google sign-in button
    if (googleButtonRef.current) {
      googleButtonRef.current.innerHTML = '';
      window.google.accounts.id.renderButton(
        googleButtonRef.current,
        { theme: 'outline', size: 'large', text: 'signin_with', type: 'standard' }
      );
    }
    // Refresh the page after sign-out
    window.location.reload();
  }

  function handleSubmit(event) {
    event.preventDefault();
    const testUser = {
      name: 'Test User',
      email: 'testuser@example.com',
      picture: 'https://www.w3schools.com/howto/img_avatar.png',
    };
    setUser(testUser);
  }

  useEffect(() => {
    const loadGoogleSignIn = () => {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: '356463161957-d7vcohppcq0uh5nvi77iuehf1aijfssg.apps.googleusercontent.com',
          callback: handleCallbackResponse,
        });
        window.google.accounts.id.renderButton(
          googleButtonRef.current,
          { theme: 'outline', size: 'large', text: 'signin_with', type: 'standard' }
        );
        window.google.accounts.id.prompt();
      }
    };

    if (!window.google) {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.defer = true;
      script.onload = loadGoogleSignIn;
      document.body.appendChild(script);
    } else {
      loadGoogleSignIn();
    }

  }, []); // Empty dependency array means this runs once when the component mounts.

  // Fetch example - Now this useEffect is separate from the Google sign-in logic
  useEffect(() => {
    fetch(`${API_URL}/your-api-endpoint`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
  }, []); // Empty dependency array to ensure this runs once when the component mounts.

  // Welcome component to show after successful login
  function Welcome() {
    return (
      <div className="welcome-message">
        <h1>Welcome, {user.name}!</h1>
        <p>We're glad to have you here.</p>
        <button onClick={handleSignOut} className="sign-out-button">Sign Out</button>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="login-container">
        {user ? (
          <Welcome />
        ) : (
          <div>
            <h2>{isSignUp ? 'Sign Up' : 'Login'}</h2>
            <form onSubmit={handleSubmit} className="login-form">
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button type="submit">{isSignUp ? 'Create Account' : 'Login'}</button>
            </form>

            {/* Divider with "OR" */}
            <div className="divider">
              <span>OR</span>
            </div>

            <div className="google-signin-wrapper">
              <div id="signInDiv" ref={googleButtonRef}></div>
            </div>

            <div className="toggle-signup">
              <p>
                {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
                <button
                  className="link-button"
                  onClick={() => setIsSignUp(!isSignUp)}
                >
                  {isSignUp ? 'Login' : 'Sign Up'}
                </button>
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;