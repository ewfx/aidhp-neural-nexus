import React, { useState } from 'react';
import './Transactions.css';
import axios from 'axios';

const Transactions = () => {
    const [transactionType, setTransactionType] = useState('credit');
    const [transaction, setTransaction] = useState({
        user: '',
        card: '',
        amount: '',
        useChip: 'Swipe',
        merchantName: '',
        merchantCity: '',
        merchantState: '',
        zip: '',
        customerID: '',
        transactionAmount: ''
    });
    const [showHistory, setShowHistory] = useState(false);
    const [historyType, setHistoryType] = useState('credit');
    const [userId, setUserId] = useState('');
    const [transactionHistory, setTransactionHistory] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setTransaction({ ...transaction, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        
        try {
            const response = await axios.post('http://localhost:5000/api/transactions', {
                transactionType,
                ...transaction,
            });
            alert(response.data.message);
            setTransaction({
                user: '',
                card: '',
                amount: '',
                useChip: 'Swipe',
                merchantName: '',
                merchantCity: '',
                merchantState: '',
                zip: '',
                customerID: '',
                transactionAmount: ''
            });
        } catch (error) {
            const errorMsg = error.response?.data?.error || 'An error occurred while processing the transaction';
            setError(errorMsg);
            alert(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    const fetchTransactionHistory = async () => {
        setLoading(true);
        setError(null);
    
        try {
            const response = await axios.get(`http://localhost:5000/api/transactions?type=${historyType}&user=${userId}`);
            setTransactionHistory(response.data.slice(0, 10));
        } catch (error) {
            const errorMsg = error.response?.status === 404 
                ? 'No records found' 
                : 'Error fetching transaction history';
            setError(errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="transactions-container">
            <h1 className="transactions-header">Transaction Portal</h1>
            
            <div className="transaction-form-container">
                <form onSubmit={handleSubmit}>
                    <div className="form-section">
                        <h2 className="form-section-title">
                            {transactionType === 'credit' ? 'Credit Card' : 'Debit Card'} Transaction
                        </h2>
                        
                        <div className="form-group">
                            <label>Transaction Type</label>
                            <select
                                name="transactionType"
                                value={transactionType}
                                onChange={(e) => setTransactionType(e.target.value)}
                            >
                                <option value="credit">Credit Card</option>
                                <option value="debit">Debit Card</option>
                            </select>
                        </div>

                        {transactionType === 'credit' ? (
                            <CreditCardForm 
                                transaction={transaction} 
                                handleInputChange={handleInputChange} 
                            />
                        ) : (
                            <DebitCardForm 
                                transaction={transaction} 
                                handleInputChange={handleInputChange} 
                            />
                        )}

                        <button type="submit" className="submit-btn" disabled={loading}>
                            {loading ? 'Processing...' : 'Submit Transaction'}
                        </button>
                    </div>
                </form>

                <button 
                    className="toggle-history-btn"
                    onClick={() => setShowHistory(!showHistory)}
                >
                    {showHistory ? 'Hide History' : 'View Transaction History'}
                </button>

                {showHistory && (
                    <TransactionHistory 
                        historyType={historyType}
                        setHistoryType={setHistoryType}
                        userId={userId}
                        setUserId={setUserId}
                        transactionHistory={transactionHistory}
                        fetchTransactionHistory={fetchTransactionHistory}
                        loading={loading}
                        error={error}
                    />
                )}
            </div>
        </div>
    );
};

const CreditCardForm = ({ transaction, handleInputChange }) => (
    <>
        <div className="form-group">
            <label>User ID</label>
            <input
                type="text"
                name="user"
                value={transaction.user}
                onChange={handleInputChange}
                required
            />
        </div>
        <div className="form-group">
            <label>Card Number</label>
            <input
                type="text"
                name="card"
                value={transaction.card}
                onChange={handleInputChange}
                required
            />
        </div>
        <div className="form-group">
            <label>Payment Method</label>
            <select
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
            <label>Amount ($)</label>
            <input
                type="number"
                name="amount"
                value={transaction.amount}
                onChange={handleInputChange}
                required
            />
        </div>
        <div className="form-group">
            <label>Merchant Name</label>
            <input
                type="text"
                name="merchantName"
                value={transaction.merchantName}
                onChange={handleInputChange}
                required
            />
        </div>
        <div className="form-row">
            <div className="form-group">
                <label>City</label>
                <input
                    type="text"
                    name="merchantCity"
                    value={transaction.merchantCity}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>State</label>
                <input
                    type="text"
                    name="merchantState"
                    value={transaction.merchantState}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <div className="form-group">
                <label>ZIP Code</label>
                <input
                    type="text"
                    name="zip"
                    value={transaction.zip}
                    onChange={handleInputChange}
                    required
                />
            </div>
        </div>
    </>
);

const DebitCardForm = ({ transaction, handleInputChange }) => (
    <>
        <div className="form-group">
            <label>Customer ID</label>
            <input
                type="text"
                name="customerID"
                value={transaction.customerID}
                onChange={handleInputChange}
                required
            />
        </div>
        <div className="form-group">
            <label>Amount (INR)</label>
            <input
                type="number"
                name="transactionAmount"
                value={transaction.transactionAmount}
                onChange={handleInputChange}
                required
            />
        </div>
    </>
);

const TransactionHistory = ({
    historyType,
    setHistoryType,
    userId,
    setUserId,
    transactionHistory,
    fetchTransactionHistory,
    loading,
    error
}) => {
    const handleSubmit = (e) => {
        e.preventDefault();
        fetchTransactionHistory();
    };

    return (
        <div className="history-section">
            <h2 className="history-header">Transaction History</h2>
            
            <form onSubmit={handleSubmit} className="history-form">
                <div className="form-row">
                    <div className="form-group">
                        <label>History Type</label>
                        <select
                            value={historyType}
                            onChange={(e) => setHistoryType(e.target.value)}
                        >
                            <option value="credit">Credit Card</option>
                            <option value="debit">Debit Card</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label>User ID</label>
                        <input
                            type="text"
                            value={userId}
                            onChange={(e) => setUserId(e.target.value)}
                            required
                        />
                    </div>
                </div>
                
                <button type="submit" className="fetch-btn" disabled={loading}>
                    {loading ? 'Loading...' : 'Fetch History'}
                </button>
            </form>

            {error && <div className="error-message">{error}</div>}

            {transactionHistory.length > 0 ? (
                <div className="history-table-container">
                    <table className="history-table">
                        <thead>
                            <tr>
                                {historyType === 'credit' ? (
                                    <>
                                        <th>User</th>
                                        <th>Card</th>
                                        <th>Amount</th>
                                        <th>Merchant</th>
                                        <th>Timestamp</th>
                                    </>
                                ) : (
                                    <>
                                        <th>Customer ID</th>
                                        <th>Amount</th>
                                        <th>Date</th>
                                        <th>Time</th>
                                    </>
                                )}
                            </tr>
                        </thead>
                        <tbody>
                            {transactionHistory.map((transaction, index) => (
                                <tr key={index}>
                                    {historyType === 'credit' ? (
                                        <>
                                            <td>{transaction.user}</td>
                                            <td>{transaction.card}</td>
                                            <td>${transaction.amount}</td>
                                            <td>{transaction.merchantName}</td>
                                            <td>{transaction.timestamp}</td>
                                        </>
                                    ) : (
                                        <>
                                            <td>{transaction.CustomerID}</td>
                                            <td>₹{transaction.TransactionAmount}</td>
                                            <td>{transaction.TransactionDate}</td>
                                            <td>{transaction.TransactionTime}</td>
                                        </>
                                    )}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            ) : (
                !loading && <div className="no-history">No transactions found</div>
            )}
        </div>
    );
};

export default Transactions;