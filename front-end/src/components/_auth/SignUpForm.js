import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Redirect } from 'react-router-dom';
import { signUp } from '../../store/session';
import './SignUpForm.css';

const SignUpForm = ({ setShowSignUpModal }) => {
  const dispatch = useDispatch();
  const user = useSelector(state => state.session.user);

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');
  const [validationErrors, setValidationErrors] = useState([]);
  const [errors, setErrors] = useState([]);

  const onSignUp = async (e) => {
    e.preventDefault();
    const errors = [];

    if (!username) errors.push("Please select a username");
    if (username.length > 20) errors.push("Please select a username less than 20 characters");
    if (!email) errors.push("Please enter your email address");
    if (!email.includes("@")) errors.push("Please provide a valid email address");
    if (!firstName) errors.push("Please enter your first name");
    if (firstName.length > 20) errors.push("First name must be less than 20 characters");
    if (!lastName) errors.push("Please enter your last name");
    if (lastName.length > 20) errors.push("Last name must be less than 20 characters");
    if (!password) errors.push("Please select a password");
    if (!repeatPassword) errors.push("Please confirm your password");

    setValidationErrors(errors);

    if (!errors.length) {
      if (password === repeatPassword) {
        const data = await dispatch(signUp(username, email, firstName, lastName, password));
        if (data) {
          const backendErrors = [];
          data.forEach(error => {
            let arr = error.split(': ');
            backendErrors.push(arr[1]);
          });
          setErrors(backendErrors);
        } else {
          setShowSignUpModal(false);
        }
      } else {
        errors.push("Please double check your confirm password.");
        setValidationErrors(errors);
      }
    }
  };

  if (user) return <Redirect to='/' />;

  return (
    <form onSubmit={onSignUp} className="sign-up-form">
      <div className="sign-up-form-container">
        <h1>Welcome to ReserveTable</h1>

        {validationErrors.length > 0 && validationErrors.map((error, idx) => (
          <div key={idx} className="sign-up-form-error-messages">{error}</div>
        ))}
        {errors.length > 0 && errors.map((error, idx) => (
          <div key={idx} className="sign-up-form-error-messages">{error}</div>
        ))}

        <input
          className="sign-up-input"
          type='text'
          name='username'
          onChange={(e) => setUsername(e.target.value)}
          value={username}
          placeholder="Username"
        />

        <input
          className="sign-up-input"
          type='text'
          name='email'
          onChange={(e) => setEmail(e.target.value)}
          value={email}
          placeholder="Email"
        />

        <input
          className="sign-up-input"
          type='text'
          name='first_name'
          onChange={(e) => setFirstName(e.target.value)}
          value={firstName}
          placeholder="First name"
        />

        <input
          className="sign-up-input"
          type='text'
          name='last_name'
          onChange={(e) => setLastName(e.target.value)}
          value={lastName}
          placeholder="Last name"
        />

        <input
          className="sign-up-input"
          type='password'
          name='password'
          onChange={(e) => setPassword(e.target.value)}
          value={password}
          placeholder="Password"
        />

        <input
          className="sign-up-input"
          type='password'
          name='repeat_password'
          onChange={(e) => setRepeatPassword(e.target.value)}
          value={repeatPassword}
          placeholder="Confirm password"
        />

        <button className="sign-up-form-button" type='submit'>Sign Up</button>
      </div>
    </form>
  );
};

export default SignUpForm;
