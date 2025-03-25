import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Transactions from './components/Transactions';
import Recommendations from './components/Recommendations';

function App() {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/" element={<Navigate to="/transactions" />} />
                    <Route path="/transactions" element={<Transactions />} />
                    <Route path="/recommendations" element={<Recommendations />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;