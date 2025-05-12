import crossStreetIcon from './icons/cross-street-icon.ico';
import operationHoursIcon from './icons/operation-hours-icon.ico';
import cuisinesIcon from './icons/cuisines-icon.ico';
import websiteIcon from './icons/website-icon.ico';
import phoneNumberIcon from './icons/phone-number-icon.ico';
import './AdditionalInfo.css';



function AdditionalInfo({ restaurant }) {

    return (
        <div className="additional-information-container">
            <div className="additional-information-header">
                Additonal information
            </div>
            <div className="additional-information">
                <div className="cross-street-container">
                    <div className="cross-street-left">
                        <img src={crossStreetIcon} alt="" className="cross-street-icon" />
                    </div>
                    <div className="cross-street-right">
                        <div className="cross-street-label">
                            Address
                        </div>
                        <div className="cross-street-details">
                            {restaurant.address}
                        </div>
                    </div>
                </div>
                <div className="operation-hours-container">
                    <div className="operation-hours-left">
                        <img src={operationHoursIcon} alt="" className="operation-hours-icon" />
                    </div>
                    <div className="operation-hours-right">
                        <div className="operation-hours-label">
                            Hours of operation
                        </div>
                        <div className="operation-hours-details">
                            {restaurant.operation_hours}
                        </div>
                    </div>
                </div>
                <div className="cuisines-container">
                    <div className="cuisines-left">
                        <img src={cuisinesIcon} alt="" className="cuisines-icon" />
                    </div>
                    <div className="cuisines-right">
                        <div className="cuisines-label">
                            Cuisines
                        </div>
                        <div className="cuisines-details">
                            {restaurant.cuisines}
                        </div>
                    </div>
                </div>
                <div className="website-container">
                    <div className="website-left">
                        <img src={websiteIcon} alt="" className="website-icon" />
                    </div>
                    <div className="website-right">
                        <div className="website-label">
                            Website
                        </div>
                        <div className="website-details">
                            <a href={restaurant.website} target="_blank" rel="noreferrer" className="website-details-font">{restaurant.website}</a>
                        </div>
                    </div>
                </div>
                <div className="phone-number-container">
                    <div className="phone-number-left">
                        <img src={phoneNumberIcon} alt="" className="phone-number-icon" />
                    </div>
                    <div className="phone-number-right">
                        <div className="phone-number-label">
                            Phone number
                        </div>
                        <div className="phone-number-details">
                            {restaurant.phone}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}



export default AdditionalInfo;