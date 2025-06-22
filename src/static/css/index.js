// Initialize and add the map
let map;
let results;

const apiUrl = 'http://localhost:5000/all';

let defaultLineColor = "#000000";

let autoEstradaColor = "#0000ff";
let itinerarioPrincipalColor = "#008000";
let itinerarioComplementarColor = "#808080";
let railwayColor = "#800000";
let hikingConnectionColor = "#800000";
let highSpeedRailwayColor = "#660066";
let waterwayRiverColor = "#33ccff";
let waterwayCoastColor = "#007fff";
let waterwayOceanColor = "#0000ff"
let planeConnectionColor = "#ff0000";

const specialHighwayNames = [
    "A20/IC23 VCI/Ponte do Freixo", "A20/IC23 VCI/Freixo Bridge",       // Portugal
    "A-376", "A-381", "A-483", "A-497", "A-8009", "A-8057", "A-8058",   // Andalucía
    "AG-51",                                                            // Galícia
    "AV-20",                                                            // Ávila
    "B-23",                                                             // Barcelona
    "CA-34", "CA-35",                                                   // Cádiz
    "CM-41",                                                            // Castilla-La Mancha
    "CO-32",                                                            // Córdoba
    "CV-80",                                                            // Comunitat Valenciana
    "EX-A1", "EX-A2",                                                   // Extremadura
    "GR-30",                                                            // Granada
    "H-30", "H-31",                                                     // Huelva
    "M-11", "M-12", "M-13/M-14", "M-13", "M-14", "M-23", "M-30",        // Comunidad de Madrid
    "M-30 - Avenida de la Ilustración", "M-30 - Bypass Sul", "M-31",
    "M-40", "M-45", "M-45/M-50", "M-50", "M-607",
    "MA-20", "MA-23",                                                   // Málaga
    "PT-10",                                                            // Puertollano
    "RM-2", "RM-16", "RM-17",                                           // Región de Murcia
    "SE-20", "SE-30", "SE-40",                                          // Seville
    "V-31", "V-31 - Avinguda d'Ausiàs March",                           // Valencia
    "VRI",                                                              // Portugal
];

function getRouteLineColor(routeName, transportMeans) {
    if (isHighway(routeName)) {
        return autoEstradaColor;
    } else if (isItinerarioPrincipal(routeName)) {
        return itinerarioPrincipalColor;
    } else if (isItinerarioComplementar(routeName)) {
        return itinerarioComplementarColor;
    } else if (isWaterway(transportMeans)) {
        return getColorByWaterway(transportMeans, routeName);
    } else if (isStandardRailway(transportMeans)) {
        return getColorByStandardRailway(routeName);
    } else if (isHighSpeedRailway(transportMeans)) {
        return highSpeedRailwayColor;
    } else if (isPlaneConnection(transportMeans)) {
        return planeConnectionColor;
    } else if (isHikingConnection(transportMeans)) {
        return hikingConnectionColor;
    } else { // Ex: Portuguese Estradas Nacionais and Spanish Carreteras del Estado
        return defaultLineColor;
    }
}

function isHighway(routeName) {
    // Portugal - auto-estrada (Ex: A1)
    // Spain - Either autovía (Ex: A-1) or autopista (Ex: AP-1)

    if ((routeName == null) || (routeName.length === 0))
        return false;

    // Generic use case - Valid for most scenarios in countries such as Portugal and France
    if (routeName.match("^A\\d+")) { // A1, A9, A99, A999, A999, etc.
        return true;
    }

    // Handles most Spanish autopistas
    if ((routeName.startsWith("AP-")) || routeName.startsWith("R-")) {
        return true;
    }

    // Handles many Spanish autovías
    if (routeName.match("^A-\\d{1,2}") && !routeName.match("^A-\\d{3,}")) { // Right - A-1, A-99. Wrong - A-100, A-9999
        return true;
    }

    // Handles special names
    return (specialHighwayNames.includes(routeName));
}

function isItinerarioPrincipal(routeName) {
    if ((routeName == null) || (routeName.length === 0))
        return false;
    return (routeName.startsWith("IP"));
}

function isItinerarioComplementar(routeName) {
    if ((routeName == null) || (routeName.length === 0))
        return false;
    else if (routeName === "Eixo Sul")
        return true;
    return (routeName.startsWith("IC"));
}

function getColorByStandardRailway(railway) {
    // Lisbon suburban railways
    if (railway.includes("Sado Line"))
        return "#0000ff";
    else if (railway.includes("Fertagus Line"))
        return "#6fa8dc";
    else if (railway.includes("Linha de Sintra") && railway.includes("CP Lisboa"))
        return "#008000";
    else if (railway.includes("Azambuja Line"))
        return "#be2c2c";
    else if (railway.includes("Cascais Line"))
        return "#ffab2e";

    // Coimbra suburban railways
    else if (railway.includes("Urbanos de Coimbra"))
        return "#3c3c3c";

    // Porto suburban railways
    else if (railway.includes("Linha de Aveiro"))
        return "#ffa700";
    else if (railway.includes("Linha do Marco de Canaveses"))
        return "#0083d7";
    else if (railway.includes("Linha de Guimarães") && !railway.includes("Intercidades")) // Only suburban stretches should receive this color
        return "#e62621";
    else if (railway.includes("Linha de Braga"))
        return "#009c5a";

    // Madrid suburban railways
    else if (railway.includes("C-1"))
        return "#66aede";
    else if (railway.includes("C-3"))
        return "#6a329f";

    // Lisbon Metro
    else if (railway.includes("Linha Vermelha - Metro de Lisboa"))
        return "#DF096F";

    // Porto Metro
    else if (railway.includes("A") && railway.includes("Metro do Porto")) // Ex: "Linhas A/B/C/E/F - Metro do Porto"
        return "#3caeef";
    else if (railway.includes("B") && railway.includes("Metro do Porto")) // Ex: "Linhas A/B/Bx/C/E/F - Metro do Porto"
        return "#e62621";
    else if (railway.includes("C") && railway.includes("Metro do Porto")) // Ex: "Linhas A/B/C/E/F - Metro do Porto"
        return "#8bc63e";
    else if (railway.includes("D") && railway.includes("Metro do Porto")) // Ex: "Linhas A/B/C/E/F - Metro do Porto"
        return "#f9c212";
    else if (railway.includes("E") && railway.includes("Metro do Porto")) // Ex: "Linhas A/B/C/E/F - Metro do Porto"
        return "#937bb8";
    else if (railway.includes("F") && railway.includes("Metro do Porto")) // Ex: "Linhas A/B/C/E/F - Metro do Porto"
        return "#f68B1f";

    // Madrid Metro
    else if (railway.includes("Line 1 - Madrid Metro"))
        return "#39b5e6";
    else if (railway.includes("Line 6 - Madrid Metro"))
        return "#999999";
    else if (railway.includes("Line 8 - Madrid Metro"))
        return "#f373b7";

    // Valencia Metro (known as Metrovalencia)
    else if (railway.includes("Linha 1 - Metrovalencia"))
        return "#fdc600";

    // Default - Likely intercity railways without assigned colors
    else
        return railwayColor;
}

function isStandardRailway(meansTransport) {
    return meansTransport === "Train" || meansTransport === "Subway";
}

function isHighSpeedRailway(meansTransport) {
    return meansTransport === "High-Speed Train";
}

function getColorByWaterway(meansTransport, routeName) {
    if (isRiverWaterway(meansTransport, routeName))
        return waterwayRiverColor;
    else if (isCoastWaterway(meansTransport, routeName))
        return waterwayCoastColor;
    else if (isOceanWaterway(meansTransport, routeName))
        return waterwayOceanColor;
    else // Default
        return waterwayRiverColor;
}

function isWaterway(meansTransport) {
    return (meansTransport === "Boat") || (meansTransport === "Ship");
}

function isRiverWaterway(meansTransport, routeName) {
    return (isWaterway(meansTransport) && (!routeName.includes("Coast")) && (meansTransport === "Boat"));
}

function isCoastWaterway(meansTransport, routeName) {
    return (isWaterway(meansTransport) && (routeName.includes("Coast")));
}

function isOceanWaterway(meansTransport, routeName) {
    return (isWaterway(meansTransport) && (!routeName.includes("Coast")) && (meansTransport === "Ship"));
}

function isPlaneConnection(meansTransport) {
    return meansTransport === "Plane";
}

function isHikingConnection(meansTransport) {
    return meansTransport === "Hiking";
}

async function createMapLine(value) {
  const lineCoordinates = [
    { lat: value[0], lng: value[1] },
    { lat: value[2], lng: value[3] },
  ];
  const meansTransport = value[4];
  const routeName = value[5];
  let color = getRouteLineColor(routeName, meansTransport);
  const line = new google.maps.Polyline({
    path: lineCoordinates,
    geodesic: true,
    strokeColor: color,
    strokeOpacity: 1.0,
    strokeWeight: 2,
  });

  line.setMap(map);
}

async function initMap() {
  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");

  // Close to the center of the Iberian Peninsula
  const position = { lat: 39.81, lng: -3.68 };

  map = new Map(document.getElementById("map"), {
    zoom: 7,
    center: position,
    mapId: "TRAVEL_MAP_ID",
  });

  results.forEach(createMapLine);
}

fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    // Display data in an HTML element
    results = data;
    initMap();
  })
  .catch(error => {
    console.error('Error:', error);
  });