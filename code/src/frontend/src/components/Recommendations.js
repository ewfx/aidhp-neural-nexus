import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Recommendations = () => {
    const [recommendations, setRecommendations] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get('http://localhost:5000/api/recommendations')
            .then(response => {
                if (Array.isArray(response.data)) {
                    setRecommendations(response.data);
                } else {
                    setError('Data is not in expected format');
                    console.error('Data is not in expected format:', response.data);
                }
            })
            .catch(error => {
                setError('There was an error fetching the recommendations');
                console.error('There was an error fetching the recommendations:', error);
            });
    }, []);

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1>Recommendations</h1>
            <table className="table">
                <thead>
                    <tr>
                        <th>Recommendation ID</th>
                        <th>Customer ID</th>
                        <th>Product</th>
                        <th>Score</th>
                    </tr>
                </thead>
                <tbody>
                    {recommendations.map(recommendation => (
                        <tr key={recommendation.RecommendationID}>
                            <td>{recommendation.RecommendationID}</td>
                            <td>{recommendation.CustomerID}</td>
                            <td>{recommendation.Product}</td>
                            <td>{recommendation.Score}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Recommendations;