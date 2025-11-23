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
    "A20/IC23 VCI/Ponte do Freixo", "A20/IC23 VCI/Freixo Bridge", "VRI",// Portugal
    "A-376", "A-381", "A-483", "A-497", "A-8009", "A-8057", "A-8058",   // Andalucía
    "AG-31", "AG-42", "AG-51", "AG-53", "AG-54",                        // Galícia
    "AS-I", "AS-II", "AS-17",                                           // Asturias
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
    "M-40", "M-45", "M-45/M-50", "M-50", "M-50/R-2", "M-607",
    "MA-20", "MA-23",                                                   // Málaga
    "O-11", "O-12", "O-14",                                             // Oviedo
    "PT-10",                                                            // Puertollano
    "RM-2", "RM-16", "RM-17",                                           // Región de Murcia
    "SE-20", "SE-30", "SE-40",                                          // Seville
    "V-11", "V-31", "V-31 - Avinguda d'Ausiàs March",                   // Valencia
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
    if (railway.includes("Sado"))
        return "#0000ff";
    else if (railway.includes("Fertagus"))
        return "#6fa8dc";
    else if (railway.includes("Sintra"))
        return "#008000";
    else if (railway.includes("Azambuja"))
        return "#be2c2c";
    else if (railway.includes("Cascais"))
        return "#ffab2e";

    // Coimbra suburban railways
    else if (railway.includes("Coimbra"))
        return "#3c3c3c";

    // Porto suburban railways
    else if (railway.includes("Aveiro Line")) // To distinguish from the Aveiro Branch Line
        return "#ffa700";
    else if (railway.includes("Marco de Canaveses"))
        return "#0083d7";
    else if (railway.includes("Guimarães"))
        return "#e62621";
    else if (railway.includes("Braga"))
        return "#009c5a";
    else if (railway.includes("Leixões"))
        return "#a887a6";

    // Madrid suburban railways
    else if (railway.includes("Cercanías Madrid")) {
        if (railway.includes("C-1") && !railway.includes("C-10"))
            return "#66aede";
        else if (railway.includes("C-2"))
            return "#008A29";
        else if (railway.includes("C-3"))
            return "#6a329f";
        else if (railway.includes("C-4"))
            return "#00289C";
        else if (railway.includes("C-5"))
            return "#FAB700";
        // Line C-6 of Madrid suburban railways was absorbed by line C-5
        else if (railway.includes("C-7"))
            return "#DE0118";
        else if (railway.includes("C-8"))
            return "#a0a0a0";
        else if (railway.includes("C-9"))
            return "#926037";
        else if (railway.includes("C-10"))
            return "#8FBE00";
    }

    // Seville suburban railways
    else if (railway.includes("Cercanías Sevilla")) {
        if (railway.includes("C-1"))
            return "#69B3E7";
        if (railway.includes("C-2"))
            return "#009739";
        if (railway.includes("C-3"))
            return "#EF3340";
        if (railway.includes("C-4"))
            return "#BB29BB";
        if (railway.includes("C-5"))
            return "#0033a0";
    }

    // Lisbon Metro
    else if (railway.includes("Lisbon Metro")) {
        if (railway.includes("Red"))
            return "#DF096F";
        else if (railway.includes("Green"))
            return "#00AA40";
        else if (railway.includes("Blue"))
            return "#4E84C4";
        else if (railway.includes("Yellow"))
            return "#F4BC18";
    }

    // Porto Metro
    else if (railway.includes("Porto Metro")) {
        if (railway.includes("A"))
            return "#3caeef";
        else if (railway.includes("B"))
            return "#e62621";
        else if (railway.includes("C"))
            return "#8bc63e";
        else if (railway.includes("D"))
            return "#f9c212";
        else if (railway.includes("E"))
            return "#937bb8";
        else if (railway.includes("F"))
            return "#f68B1f";
    }

    // Metro Sul do Tejo (== South Tagus)
    else if (railway.includes("Metro Sul do Tejo")) {
        // Has Y-shape and 3 lines, most stations are served by 2 lines
        if (railway.includes("1") && railway.includes("3")) // Display color of line 1
            return "#218FCE";
        else if (railway.includes("1") && railway.includes("2")) // Display color of line 2
            return "#F7941C";
        else // Display color of line 3
            return "#A2A730";
    }

    // Madrid Metro
    if (railway.includes("Madrid Metro")) {
        if (railway.includes("1") && !railway.includes("10") && !railway.includes("11") && !railway.includes("12"))
            return "#39b5e6";
        else if (railway.includes("2"))
            return "#fb0f0c";
        else if (railway.includes("3"))
            return "#FFDF00";
        else if (railway.includes("4"))
            return "#824100";
        else if (railway.includes("5"))
            return "#96bf0d";
        else if (railway.includes("6"))
            return "#999999";
        else if (railway.includes("7"))
            return "#ff8501";
        else if (railway.includes("8"))
            return "#f373b7";
        else if (railway.includes("9"))
            return "#9F1F99";
        else if (railway.includes("10"))
            return "#003da6";
        else if (railway.includes("11"))
            return "#00953b";
        else if (railway.includes("12"))
            return "#a19200";
        else if (railway.includes("R"))
            return "#ffffff";
        else if (railway.includes("ML1"))
            return "#287ee2";
        else if (railway.includes("ML2"))
            return "#aa148e";
        else if (railway.includes("ML3"))
            return "#ff4336";
        else if (railway.includes("ML4"))
            return "#77ba26";
    }

    // Valencia Metro (known as Metrovalencia)
    else if (railway.includes("Metrovalencia")) {
        if (railway.includes("1") && !railway.includes("10"))
            return "#E6B036";
        else if (railway.includes("2"))
            return "#D23983";
        else if (railway.includes("3"))
            return "#C21E2D";
        else if (railway.includes("4"))
            return "#0F4583";
        else if (railway.includes("5"))
            return "#008358";
        else if (railway.includes("6"))
            return "#80629F";
        else if (railway.includes("7"))
            return "#DB8319";
        else if (railway.includes("8"))
            return "#41B1CB";
        else if (railway.includes("9"))
            return "#AC7D4E";
        else if (railway.includes("10"))
            return "#B3CB6D";
    }

    // Seville Metro
    else if (railway.includes("Seville Metro")) {
        if (railway.includes("1")) {
            return "#01820b";
        }
    }

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