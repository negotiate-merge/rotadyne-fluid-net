import React, { useState, useEffect, useCallback } from 'react';
import {
    APIProvider,
    Map,
    AdvancedMarker,
    Pin,
    InfoWindow,
    useAdvancedMarkerRef,
} from "@vis.gl/react-google-maps";

function App() {
    const [data, setData] = useState([{}]);

    useEffect(() => {
        const intervalId = setInterval(() => {
            fetch("/devices")
            .then((res) => res.json())
            .then((data) => {
                setData(data);
                console.log(data);
            })
            .catch((error) => {
                console.error("Error fetching data: ", error);
            })
        }, 5000);

        return () => clearInterval(intervalId);

    }, []);

    const api_key = "***REMOVED***";
    const map_id = "1a3de3b04bbcad29";

    /* HAVE A LOOK AT 
    https://developers.google.com/maps/documentation/javascript/advanced-markers/basic-customization
    to get the markers on the map via a loop
    */

    return (
        <APIProvider apiKey={api_key}>
            <div style={{height: "100vh"}}>
                <Map 
                    // zoom={9} 
                    // center={pumps[0][0]}
                    defaultZoom={16}
                    defaultCenter={{ lat: -33.707055119346386, lng: 151.14593296712843 }}
                    mapId={map_id}
                    gestureHandling={'greedy'}
                    disableDefaultUI={false}
                >
                    {data.map((point) => (
                        <Marker key={point.devId} point={point} />
                    ))}
                </Map>
            </div>
        </APIProvider>
    );
}


function pinColor(point) {
    if (point.emergency) {
        return "#ED1F1F";
    } else if (point.pumping) {
        return "green";
    } else {
        return "orange";
    }
}

const Marker = ({point}) => {

    const [markerRef, marker] = useAdvancedMarkerRef();
    const [infoWindowShown, setInfoWindowShown] = useState(false); // Switch for info-window

    const handleMarkerClick = useCallback(() => setInfoWindowShown(isShown => !isShown), []);
    const handleClose = useCallback(() => setInfoWindowShown(false),[]);

    if (!point.lat || !point.lng) {
        console.error('Latitude or longitude is missing for point', point);
        return null;
    }

    return (
        <AdvancedMarker
            ref={markerRef}
            position={{ lat: point.lat, lng: point.lng }} 
            key={point.devId}
            title={point.title}
            onClick={handleMarkerClick}
        >
            <Pin background={ pinColor(point) } borderColor={ pinColor(point) } glyphColor="black" />
            {infoWindowShown && 
                <InfoWindow className="iwColumn" anchor={marker} onClose={handleClose}>
                    <h3>{point.title}</h3>
                    <table>
                        <tbody>
                            <tr>
                                <td>Full:</td>
                                <td>{ (point.full) ? "Yes" : "No" }</td>
                            </tr>
                            <tr>
                                <td>Emergency:</td>
                                <td>{ (point.emergency) ? "Yes" : "No" }</td>
                            </tr>
                            <tr>
                                <td>Pumping:</td>
                                <td>{ (point.pumping) ? "Yes" : "No" }</td>
                            </tr>
                            <tr>
                                <td>Current:</td>
                                <td>{point.current} mA</td>
                            </tr>
                            <tr>
                                <td>Switch Pump:</td>
                                <td>
                                    <button type="submit" onClick={() => {
                                        let xhr = new XMLHttpRequest();
                                        let url = "/pump_switch";
                                        xhr.open("POST", url, true);
                                        xhr.setRequestHeader("Content-Type", "application/json")
                                        xhr.onreadystatechange = function () {
                                            if (xhr.readyState === 4 && xhr.status === 200) {
                                                XPathResult.innerHTML = this.response.Text;
                                            }
                                        };
                                        var data = JSON.stringify(point);
                                        xhr.send(data);
                                    }
                                    }>{(point.pumping) ? "Off" : "On"}</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
            </InfoWindow> }
        </AdvancedMarker>
    );
};

export default App

