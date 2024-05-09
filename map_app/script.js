/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
// import { PinElement } from "@googlemaps/markerclustererplus";
async function initMap() {
    // Request needed libraries.
    /*
    const home = { lat: -33.707055119346386, lng: 151.14593296712843 };
    const dog_lost = { lat: -33.703436, lng: 151.152421 };
    const dog_found = { lat: -33.703273, lng: 151.149308 };
    */

    const { PinElement } = await google.maps.importLibrary("marker");
    var p_running = new PinElement({
        borderColor: "#2a6900",
        background: "#66ff00",
        glyphColor: "#000000",
    })

    var p_standby = new PinElement({
        borderColor: "#996300",
        background: "#ffa600",
        glyphColor: "#000000",
    })

    var p_emergency = new PinElement({
        borderColor: "#620808",
        background: "#ff0000",
        glyphColor: "#000000",
    })

    const pumps = [
        [{ lat: -33.707055119346386, lng: 151.14593296712843 }, "Home"],
        [{ lat: -33.703436, lng: 151.152421 }, "Lost"],
        [{ lat: -33.703273, lng: 151.149308 }, "Found"],
    ]

    const { Map } = await google.maps.importLibrary("maps");
    const map = new Map(document.getElementById("map"), {
      center: { lat: -33.704786307407275, lng: 151.14699046030896 },
      zoom: 17,
      mapId: "1a3de3b04bbcad29",
    });

    const infoWindow = new google.maps.InfoWindow();

    pumps.forEach(([position, title], i) => {
        const marker = new google.maps.Marker({
            position,
            map,
            title: `${i + 1}. ${title}`,
            label: `${title}`,
            optimized: false,
        });

        marker.addListener("click", () => {
            infoWindow.close();
            infoWindow.setContent(marker.getTitle());
            infoWindow.open(marker.getMap(), marker);
        });
    });
}

initMap();



    /*
    const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
    const m_home = new AdvancedMarkerElement({
      map,
      title: "The dog house.",
      position: home,
      content: p_standby.element,
    });

    const m_dog_lost = new AdvancedMarkerElement({
        map,
        title: "Dog lost here.",
        position: dog_lost,
        content: p_emergency.element,
      });

    const m_dog_found = new AdvancedMarkerElement({
        map,
        title: "Dog found here!",
        position: dog_found,
        content: p_running.element,
    });

    

    const marker = new google.maps.Marker({
        position: { lat: -33.70654973196368, lng: 151.14665733509585 },
        map: map,
        label: "Pump 1",
    })
    */
  
  /*

function initMap() {
    const home = { lat: -33.707055119346386, lng: 151.14593296712843 };
    const dog_lost = { lat: -33.703436, lng: 151.152421 };
    const dog_found = { lat: -33.703273, lng: 151.149308 };

    const running = "./paint_3d/green_30x30.png"
    const standby = "./paint_3d/orange_30x30.png"
    const emergency = "./paint_3d/red_30x30.png"

    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 17,
      center: home,
    });
  
    new google.maps.Marker({
        position: home,
        map,
        title: "The dog house.",
        icon: standby,
      });

    new google.maps.Marker({
      position: dog_lost,
      map,
      title: "Dog lost here.",
      icon: emergency,
    });

    new google.maps.Marker({
        position: dog_found,
        map,
        title: "Dog found here!",
        icon: running,
      });
  }
  
  window.initMap = initMap;
  */