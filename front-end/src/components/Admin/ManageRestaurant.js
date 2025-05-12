import React, { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import './ManageRestaurant.css';

function ManageRestaurant() {
  const [restaurants, setRestaurants] = useState([]);
  const user = useSelector(state => state.session.user);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);

  useEffect(() => {
    fetch("/api/admin/restaurants", { credentials: "include" })
      .then(res => res.json())
      .then(setRestaurants);
  }, []);

  const viewDetails = (restaurant) => {
    setSelectedRestaurant(restaurant);
  };

  const approveRestaurant = (id) => {
    fetch(`/api/admin/approve/${id}`, {
      method: "PATCH",
      credentials: "include"
    }).then(() => {
      return fetch("/api/admin/restaurants", { credentials: "include" });
    }).then(res => res.json())
      .then(setRestaurants);
  };

  const deleteRestaurant = (id) => {
    fetch(`/api/admin/delete/${id}`, {
      method: "DELETE",
      credentials: "include"
    }).then(() => {
      setRestaurants(prev => prev.filter(r => r.id !== id));
    });
  };

  if (!user?.is_admin) {
    return <p>Access denied.</p>;
  }

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h2>🏪 Manage Restaurants</h2>
        <p>Approve or delete pending restaurants submitted by managers.</p>
      </div>

      <div className="dashboard-card">
        <table className="analytics-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Approved</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {restaurants.map(r => (
              <tr key={r.id}>
                <td>{r.name}</td>
                <td>{r.is_approved ? "✅ Yes" : "❌ No"}</td>
                <td>
                  <div className="action-buttons">
                    <button onClick={() => viewDetails(r)} className="admin-btn details-btn">View Details</button>
                    {!r.is_approved && (
                        <button onClick={() => approveRestaurant(r.id)}
                                className="admin-btn approve-btn">Approve</button>
                    )}
                    <button onClick={() => deleteRestaurant(r.id)} className="admin-btn delete-btn">Delete</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedRestaurant && (
          <div className="modal-overlay" onClick={() => setSelectedRestaurant(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <h2 className="modal-title">{selectedRestaurant.name}</h2>

              <img
                  src={selectedRestaurant.preview_img}
                  alt={`${selectedRestaurant.name} preview`}
                  className="modal-image"
              />

              <div className="modal-details">
                <p><strong>Cuisines:</strong> {selectedRestaurant.cuisines}</p>
                <p><strong>Cost:</strong> {selectedRestaurant.cost}</p>
                <p><strong>Neighborhood:</strong> {selectedRestaurant.neighborhood}</p>
                <p><strong>Dress Code:</strong> {selectedRestaurant.dress_code}</p>
                <p><strong>Description:</strong></p>
                <p className="modal-description">{selectedRestaurant.description}</p>
                <p><strong>Website:</strong> <a href={selectedRestaurant.website} target="_blank"
                                                rel="noreferrer">{selectedRestaurant.website}</a></p>
              </div>

              <button className="admin-btn close-btn" onClick={() => setSelectedRestaurant(null)}>Close</button>
            </div>
          </div>
      )}

    </div>
  );
}

export default ManageRestaurant;
