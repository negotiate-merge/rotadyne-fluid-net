import React, { useState, useEffect } from 'react';
import {
    APIProvider,
    Map,
    AdvancedMarker,
    Pin,
    InfoWindow,
} from "@vis.gl/react-google-maps";

function App() {
    const [data, setData] = useState([{}]);

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


    const api_key = "***REMOVED***";
    const map_id = "1a3de3b04bbcad29";
    const [open, setOpen] = useState(false); // Switch for info-window

    const pumps = [
        [{ lat: -33.707055119346386, lng: 151.14593296712843 }, "Home"],
        [{ lat: -33.703436, lng: 151.152421 }, "Lost"],
        [{ lat: -33.703273, lng: 151.149308 }, "Found"],
    ]

    return (
        <APIProvider apiKey={api_key}>
            <div style={{height: "100vh"}}>
                <Map 
                    // zoom={9} 
                    // center={pumps[0][0]}
                    defaultZoom={16}
                    defaultCenter={pumps[0][0]}
                    mapId={map_id}
                    gestureHandling={'greedy'}
                    disableDefaultUI={true}
                >
                    <AdvancedMarker 
                        position={pumps[0][0]}
                        title={pumps[0][1]}
                        onClick={() => setOpen(true)}>
                            <Pin background={"grey"} borderColor={"green"} glyphColor={"purple"} />
                    </AdvancedMarker>
                    {open && <InfoWindow 
                                position={pumps[0][0]} 
                                onCloseClick={() => setOpen(false)}
                                >
                                    <p>{pumps[0][1]}</p>
                                </InfoWindow> }
                </Map>
            </div>
        </APIProvider>
    );
}

/* {(typeof data.members === 'undefined') ? (
                <p>Loading...</p>
            ) : (
                data.members.map((member, i) => (
                    <p key={i}>{member}</p>
                ))
            )} 
*/

export default App

