import React, { useEffect, useState } from 'react';
import './MenuDialog.css';

const MenuDialog = ({ restaurantId, onClose }) => {
    const [menuItems, setMenuItems] = useState([]);

    useEffect(() => {
        fetch(`/api/restaurant-manager/public-menu-items/${restaurantId}`)
            .then(res => res.json())
            .then(data => setMenuItems(data))
            .catch(err => {
                console.error("Error fetching menu items:", err);
                setMenuItems([]);
            });
    }, [restaurantId]);

    return (
        <div className="menu-dialog-overlay">
            <div className="menu-dialog-box">
                <button className="close-btn" onClick={onClose}>X</button>
                <h2>Menu</h2>

                {menuItems.length === 0 ? (
                    <p>No items yet.</p>
                ) : (
                    <table className="menu-table">
                        <thead>
                            <tr>
                                <th>Item</th>
                                <th>Description</th>
                                <th>Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            {menuItems.map(item => (
                                <tr key={item.id}>
                                    <td>{item.name}</td>
                                    <td>{item.description}</td>
                                    <td>${item.price}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default MenuDialog;
