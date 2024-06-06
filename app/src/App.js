import React, { useState, useEffect, useCallback } from 'react';
import {
    APIProvider,
    Map,
    AdvancedMarker,
    Pin,
    InfoWindow,
    useAdvancedMarkerRef,
} from "@vis.gl/react-google-maps";

const pumps = [
    {   
        devId: "a84041e081893e7f",
        title: "Home",
        lat: -33.707055119346386,
        lng: 151.14593296712843,
        full: 0,
        emergency: 0,
        current: 0,
    },
    {   
        devId: "a84041e081893e80",
        title: "Lost",
        lat: -33.703436,
        lng: 151.152421,
        full: 0,
        emergency: 0,
        current: 0,
    },
    {   
        devId: "a84041e081893e81",
        title: "Found",
        lat: -33.703273,
        lng: 151.149308,
        full: 0,
        emergency: 0,
        current: 0,
    },
]

function App() {
    const [data, setData] = useState([{}]);

    useEffect(() => {
        const intervalId = setInterval(() => {
            fetch("/devices").then(
                res => res.json()
            ).then(
                data => {
                    setData(data);
                    // console.log(data);
                }
            ).catch(error => {
                console.error("Error fetching data: ", error);
            })
        }, 10000)

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
                    disableDefaultUI={true}
                >
                    
                    {/*pumps.map(pumps => console.log("JS Pumps: ", pumps))*/}
                    
                    {data.map(points => {// changed pumps.map to data.map
                        
                        <Marker key={points.devId} point={points} />
                    })}
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

    const handleMarkerClick = useCallback(() =>
        setInfoWindowShown(isShown => !isShown),
    []
    );

    const handleClose = useCallback(() => setInfoWindowShown(false),[]);
    console.log(point)

    return <>
        {
            
            <AdvancedMarker
                ref={markerRef}
                position={ { lat: point.lat, lng: point.lng }} 

                title={point.title}
                onClick={handleMarkerClick}>
                    <Pin background={ pinColor(point) } borderColor={ pinColor(point) } glyphColor={ "black" } />
                {infoWindowShown && <InfoWindow className="iwColumn"
                    anchor={marker} 
                    /*position={{ lat: point.lat, lng: point.lng }} */
                    onClose={handleClose}
                    >
                        <h3>{point.title}</h3>
                        <table>
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
                                <td>Pump:</td>
                                <td><button>Switch</button></td>
                            </tr>
                        </table>
                </InfoWindow> }
            </AdvancedMarker>}
    </>
}

// taken out of return statement above                      key={point.devId}


export default App

