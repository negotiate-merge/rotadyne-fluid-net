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

    /*
    useEffect(() => {
        fetch("/members").then(
            res => res.json()
        ).then(
            data => {
                setData(data);
                console.log(data);
            }
        ).catch(error => {
            console.error("Error fetching data: ", error);
        })
    }, []);
    */


    const api_key = "***REMOVED***";
    const map_id = "1a3de3b04bbcad29";

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
                    <Markers points={pumps} />
                </Map>
            </div>
        </APIProvider>
    );
}


const Markers = ({points}) => {

    const [markerRef, marker] = useAdvancedMarkerRef();
    const [infoWindowShown, setInfoWindowShown] = useState(false); // Switch for info-window

    const handleMarkerClick = useCallback(() =>
        setInfoWindowShown(isShown => !isShown),
    []
    );

    const handleClose = useCallback(() => setInfoWindowShown(false),[]);

    return <>
        {points.map(point => 
            <AdvancedMarker
                ref={markerRef}
                position={{ lat: point.lat, lng: point.lng }} 
                key={point.devId}
                title={point.title}
                onClick={handleMarkerClick}>
                    <Pin background={"grey"} borderColor={"green"} glyphColor={"purple"} />
                {infoWindowShown && <InfoWindow
                    anchor={marker} 
                    /*position={{ lat: point.lat, lng: point.lng }} */
                    onClose={handleClose}
                    >
                        <p>{point.title}</p>
                </InfoWindow> }
            </AdvancedMarker>)}
    </>
}

export default App

