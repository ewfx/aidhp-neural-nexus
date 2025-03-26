import React, { useEffect, useState } from 'react';
import './Recommendations.css';
import axios from 'axios';

const Recommendations = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [userId, setUserId] = useState('');
    const [submitStatus, setSubmitStatus] = useState(null);

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/recommendations');
                setRecommendations(response.data);
            } catch (err) {
                console.error('Error fetching recommendations:', err);
                setError('Failed to load recommendations. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitStatus('Submitting...');
        try {
            const response = await axios.get(`http://localhost:5000/api/collaborativeRec?user=${userId}`);
            setSubmitStatus('Submitted successfully!');
            console.log('Response:', response.data);
        } catch (err) {
            console.error('Error submitting UserID:', err);
            setSubmitStatus('Failed to submit. Please try again.');
        }
    };

    if (loading) {
        return (
            <div className="container recommendations-page">
                <div className="loading-spinner"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="container recommendations-page">
                <div className="error-message">{error}</div>
            </div>
        );
    }

    return (
        <div className="container recommendations-page">
            <h1 className="section-title">Personalized Recommendations</h1>
            <div className="recommendations-grid">
                {recommendations.length > 0 ? (
                    recommendations.map((rec, index) => (
                        <RecommendationCard 
                            key={index}
                            recommendations={rec.recommendations}
                            index={index}
                        />
                    ))
                ) : (
                    <div className="empty-state">
                        No recommendations available at the moment.
                    </div>
                )}
            </div>
            
            {/* Add the form at the bottom center */}
            <div className="user-id-form-container">
                <form onSubmit={handleSubmit} className="user-id-form">
                    <div className="form-group">
                        <label htmlFor="userId">UserID:</label>
                        <input
                            type="text"
                            id="userId"
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            placeholder="Enter your UserID"
                            required
                        />
                    </div>
                    <button type="submit" className="submit-btn">
                        Submit
                    </button>
                    {submitStatus && <div className="submit-status">{submitStatus}</div>}
                </form>
            </div>
        </div>
    );
};

const RecommendationCard = ({ recommendations, index }) => {
    const colors = [
        'linear-gradient(135deg, #ff4e50, #f9d423)',
        'linear-gradient(135deg, #ff416c, #ff4b2b)',
        'linear-gradient(135deg, #ff5f6d, #ffc371)',
        'linear-gradient(135deg, #ff4b1f, #ff9068)'
    ];
    
    return (
        <div 
            className="recommendation-card"
            style={{ background: colors[index % colors.length] }}
        >
            <div className="card-content">
                <p className="product-desc">{recommendations}</p>
            </div>
            <div className="card-actions">
                <button className="action-btn">Learn More</button>
            </div>
        </div>
    );
};

export default Recommendations;