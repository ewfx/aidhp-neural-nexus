import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
// import Chatbot from './components/Chatbot'; // Create this component if not already created
import Transactions from './components/Transactions';
import Recommendations from './components/Recommendations';
import Chatbot from './components/Chatbot'

function App() {
    return (
        <Router>
            <Navbar />
            <div className="main-content">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/chatbot" element={<Chatbot />} />
                    <Route path="/transactions" element={<Transactions />} />
                    <Route path="/recommendations" element={<Recommendations />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;