import { useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import LogoutButton from "../_auth/LogoutButton";
import pointsGraph from '../../icons/points-graph.ico'
import './ProfileButtonMenu.css'


function ProfileButtonMenu({ setShowSignInModal }) {
    const history = useHistory();
    const sessionUser = useSelector(state => state.session.user);

    const routeToDiningDashboard = () => {
        history.push(`/users/${sessionUser.id}/dining-dashboard`);
    }

    const routeToSavedRestaurants = () => {
        history.push(`/users/${sessionUser.id}/dining-dashboard?view=saved-restaurants`);
    }


    return (
        <div className="profile-drop-down-menu">
            <div className="profile-drop-down-bottom">
                <div className="greeting">Hello, {sessionUser.first_name}!</div>

                <div className="profile-drop-button my-dining-history" onClick={routeToDiningDashboard}>
                    <span className="spacing-down profiile-drop-button-left">My Reservations</span>
                </div>
                <div className="profile-drop-button my-saved-restaurants" onClick={routeToSavedRestaurants}>
                    <span className="spacing-down profiile-drop-button-left">My Saved Restaurants</span>
                </div>
                <div className="profile-log-out-button"><LogoutButton setShowSignInModal={setShowSignInModal} /></div>
            </div>
        </div>
    )
}



export default ProfileButtonMenu;