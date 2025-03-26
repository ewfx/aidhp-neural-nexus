import React from 'react';
import './Home.css';

const Home = () => {
    return (
        <div className="home-container">
            <div className="hero-section">
                <h1 className="hero-title">
                    <span className="title-highlight">I&P</span> Technology Hackathon 2025
                </h1>
                <p className="hero-subtitle">AI-Driven Hyper Personalization and Recommendation</p>
            </div>

            <div className="features-container">
                <div className="feature-card">
                    <div className="card-icon">👥</div>
                    <h3>Team Name</h3>
                    <p className="feature-text">Neural-Nexus</p>
                </div>

                <div className="feature-card">
                    <div className="card-icon">🌟</div>
                    <h3>Team Members</h3>
                    <div className="team-grid">
                        <p>Sarvesh</p>
                        <p>Suren</p>
                        <p>Vedant</p>
                        <p>Anshu</p>
                    </div>
                </div>

                <div className="feature-card">
                    <div className="card-icon">🎥</div>
                    <h3>Demo Video</h3>
                    <p className="feature-text">
                        <a href="#" className="video-link">Watch our demo</a>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Home;