import React, { useState } from 'react';
import './Transactions.css';
import axios from 'axios';
import moment from 'moment'; // Import moment.js for date formatting

const Transactions = () => {
    const [transactionType, setTransactionType] = useState('credit');
    const [showHistory, setShowHistory] = useState(false);
    const [historyType, setHistoryType] = useState('credit');
    const [userId, setUserId] = useState('');
    const [transactionHistory, setTransactionHistory] = useState([]);
    const initialTransactionState = {
        user: '',
        card: '',
        amount: '',
        useChip: 'Swipe', // Default value
        merchantName: '',
        merchantCity: '',
        merchantState: '',
        zip: ''
    };
    const [transaction, setTransaction] = useState(initialTransactionState);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setTransaction({ ...transaction, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const transactionData = {
            ...transaction,
            transactionType,
            timestamp: moment().format('YYYY-MM-DD HH:mm:ss') // Format timestamp
        };

        try {
            const response = await axios.post('http://localhost:5000/api/transactions', transactionData);
            console.log(response.data);
            setTransaction(initialTransactionState); // Clear form fields after submission
        } catch (error) {
            console.error('Error adding transaction:', error);
        }
    };

    const toggleHistory = () => {
        setShowHistory(!showHistory);
    };

    const fetchTransactionHistory = async () => {
        try {
            const response = await axios.get(`http://localhost:5000/api/transactions?type=${historyType}&user=${userId}`);
            setTransactionHistory(response.data.slice(0, 10)); // Get the latest 10 transactions
        } catch (error) {
            console.error('Error fetching transaction history:', error);
        }
    };

    const handleHistorySubmit = (e) => {
        e.preventDefault();
        fetchTransactionHistory();
    };

    return (
        <div className="container transaction-page">
            <h1 className="text-center text-danger">Transaction Page</h1>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Transaction Type:</label>
                    <select
                        className="form-control"
                        name="transactionType"
                        value={transactionType}
                        onChange={(e) => setTransactionType(e.target.value)}
                    >
                        <option value="credit">Credit Card</option>
                        <option value="debit">Debit Card</option>
                    </select>
                </div>

                {transactionType === 'credit' && (
                    <>
                        <div className="form-group">
                            <label>User:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="user"
                                value={transaction.user}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Card:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="card"
                                value={transaction.card}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Use Chip:</label>
                            <select
                                className="form-control"
                                name="useChip"
                                value={transaction.useChip}
                                onChange={handleInputChange}
                                required
                            >
                                <option value="Swipe">Swipe</option>
                                <option value="Online">Online</option>
                            </select>
                        </div>
                        <div className="form-group">
                            <label>Amount:</label>
                            <input
                                className="form-control"
                                type="number"
                                name="amount"
                                value={transaction.amount}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Merchant Name:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="merchantName"
                                value={transaction.merchantName}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Merchant City:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="merchantCity"
                                value={transaction.merchantCity}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Merchant State:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="merchantState"
                                value={transaction.merchantState}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Zip:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="zip"
                                value={transaction.zip}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                    </>
                )}

                {transactionType === 'debit' && (
                    <>
                        <div className="form-group">
                            <label>User ID:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="user"
                                value={transaction.user}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Card:</label>
                            <input
                                className="form-control"
                                type="text"
                                name="card"
                                value={transaction.card}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>Amount:</label>
                            <input
                                className="form-control"
                                type="number"
                                name="amount"
                                value={transaction.amount}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                    </>
                )}

                <button type="submit" className="btn btn-danger btn-block">Submit Transaction</button>
            </form>

            <button className="btn btn-outline-danger btn-block toggle-history" onClick={toggleHistory}>
                {showHistory ? 'Hide' : 'Show'} Transaction History
            </button>

            {showHistory && (
                <>
                    <form onSubmit={handleHistorySubmit}>
                        <div className="form-group mt-3">
                            <label>History Type:</label>
                            <select
                                className="form-control"
                                value={historyType}
                                onChange={(e) => setHistoryType(e.target.value)}
                            >
                                <option value="credit">Credit Card</option>
                                <option value="debit">Debit Card</option>
                            </select>
                        </div>
                        <div className="form-group mt-3">
                            <label>User ID:</label>
                            <input
                                className="form-control"
                                type="text"
                                value={userId}
                                onChange={(e) => setUserId(e.target.value)}
                                required
                            />
                        </div>
                        <button type="submit" className="btn btn-danger btn-block">Fetch History</button>
                    </form>
                    <table className="table mt-4">
                        <thead>
                            <tr>
                                <th>User</th>
                                <th>Card</th>
                                <th>Amount</th>
                                <th>Merchant Name</th>
                                <th>Timestamp</th>
                            </tr>
                        </thead>
                        <tbody>
                            {transactionHistory.map((transaction, index) => (
                                <tr key={index}>
                                    <td>{transaction.user}</td>
                                    <td>{transaction.card}</td>
                                    <td>${transaction.amount}</td>
                                    <td>{transaction.merchantName}</td>
                                    <td>{transaction.timestamp}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </>
            )}
        </div>
    );
};

export default Transactions;