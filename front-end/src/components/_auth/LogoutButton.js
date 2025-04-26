import React from 'react';
import { useHistory } from 'react-router-dom';
import { useDispatch } from 'react-redux';


const LogoutButton = ({ setShowSignInModal }) => {
  const dispatch = useDispatch();
  const history = useHistory();
  

  return (
      <div  onClick={onLogout}>
        Sign out
      </div>
  )
};

export default LogoutButton;