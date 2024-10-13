import React, { useState } from 'react';
import Login from './components/Login';
import ProjectList from './components/ProjectList';

const App = () => {
  const [token, setToken] = useState(null);

  return (
    <div>
      {token ? (
        <ProjectList token={token} />
      ) : (
        <Login setToken={setToken} />
      )}
    </div>
  );
};

export default App;
