import React from 'react';
import Design from './pages/Design'
import Home from './pages/Home.jsx'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Design />}>
          <Route path = "/" element={<Home/>} />
        </Route>
      </Routes>
    </BrowserRouter>
    );
  }

export default App;
