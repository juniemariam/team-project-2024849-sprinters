import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import './AdminDashboard.css';

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const user = useSelector(state => state.session.user);

  useEffect(() => {
    fetch("/api/admin/analytics", {
      credentials: "include"
    })
      .then(res => res.json())
      .then(setStats);
  }, []);

  if (!user?.is_admin) return <p>Access denied.</p>;
  if (!stats) return <p>Loading...</p>;

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h2>📊 Reservation Analytics (Last 30 Days)</h2>
        <p>Insights from recent reservations across all restaurants.</p>
      </div>

      <div className="dashboard-card">
        <div className="summary-metrics">
          <p><strong>Total Reservations:</strong> {stats.total}</p>
          <p><strong>Average Party Size:</strong> {stats.average_party_size}</p>
          <p><strong>Top Restaurant:</strong> {stats.top_restaurant || "—"}</p>
        </div>

        <table className="analytics-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Reservations</th>
            </tr>
          </thead>
          <tbody>
            {stats.daily.map(({ date, count }) => (
              <tr key={date}>
                <td>{date}</td>
                <td>{count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AdminDashboard;