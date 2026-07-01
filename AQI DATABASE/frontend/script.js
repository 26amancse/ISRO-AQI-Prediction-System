/* ==========================================================
   ISRO AQI DASHBOARD
========================================================== */

const API_URL = "http://127.0.0.1:8000/predict";

/* ==========================================================
   MAP
========================================================== */

const map = L.map("map").setView([28.6139, 77.2090], 10);

L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        attribution: "&copy; OpenStreetMap contributors",
        maxZoom: 19
    }
).addTo(map);

const marker = L.marker([28.6139, 77.2090]).addTo(map);

marker.bindPopup("<b>Delhi</b><br>Loading AQI...");


/* ==========================================================
   AQI STATUS
========================================================== */

function getAQIStatus(aqi){

    if(aqi<=50) return "Good";

    if(aqi<=100) return "Satisfactory";

    if(aqi<=200) return "Moderate";

    if(aqi<=300) return "Poor";

    if(aqi<=400) return "Very Poor";

    return "Severe";

}


/* ==========================================================
   AQI COLOR
========================================================== */

function getAQIColor(aqi){

    if(aqi<=50) return "#22c55e";

    if(aqi<=100) return "#84cc16";

    if(aqi<=200) return "#f59e0b";

    if(aqi<=300) return "#fb923c";

    if(aqi<=400) return "#ef4444";

    return "#7f1d1d";

}


/* ==========================================================
   HEALTH MESSAGE
========================================================== */

function getHealthMessage(aqi){

    if(aqi<=50)
        return "Excellent air quality. Enjoy outdoor activities.";

    if(aqi<=100)
        return "Air quality is acceptable for most people.";

    if(aqi<=200)
        return "Sensitive groups should limit prolonged outdoor activity.";

    if(aqi<=300)
        return "Wear a mask when outdoors.";

    if(aqi<=400)
        return "Avoid unnecessary outdoor activities.";

    return "Stay indoors whenever possible.";

}


/* ==========================================================
   LIVE CLOCK
========================================================== */

function updateClock(){

    const now = new Date();

    document.getElementById("time").textContent =
        now.toLocaleString();

}

updateClock();

setInterval(updateClock,1000);


/* ==========================================================
   STARTUP
========================================================== */

console.log("================================");

console.log("ISRO AQI Dashboard Started");

console.log("Waiting for Backend...");

console.log("================================");
/* ==========================================================
   FETCH LIVE DATA
========================================================== */

async function fetchAQI() {

    try {

        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Backend not responding");
        }

        const data = await response.json();

        console.log("AQI Data:", data);

        updateDashboard(data);

    }

    catch (err) {

        console.error("Fetch Error:", err);

    }

}

/* ==========================================================
   UPDATE DASHBOARD
========================================================== */

function updateDashboard(data) {

    const aqi = Math.round(data.aqi);

    // ================= AQI =================

    document.getElementById("aqiValue").textContent = aqi;

    document.getElementById("aqiCard").textContent = aqi;

    document.getElementById("aqiStatus").textContent =
        getAQIStatus(aqi);

    const color = getAQIColor(aqi);

    document.querySelector(".aqi-circle").style.background = color;

    document.getElementById("aqiStatus").style.background = color;

    document.querySelector(".progress-bar").style.width =
        Math.min(aqi / 500 * 100, 100) + "%";


    // ================= WEATHER =================

    document.getElementById("temperature").textContent =
        data.temperature.toFixed(1) + "°C";

    document.getElementById("pressure").textContent =
        Math.round(data.pressure) + " Pa";

    document.getElementById("wind").textContent =
        data.wind.toFixed(2) + " m/s";

    document.getElementById("humidity").textContent =
        "--";

    document.getElementById("dewpoint").textContent =
        "--";


    // ================= POLLUTANTS =================

    document.getElementById("hcho").textContent =
        Number(data.hcho).toExponential(3);

    document.getElementById("no2").textContent =
        data.no2 == null
        ? "N/A"
        : Number(data.no2).toExponential(3);

    document.getElementById("co").textContent =
        Number(data.co).toFixed(5);

    document.getElementById("so2").textContent =
        Number(data.so2).toFixed(6);

    document.getElementById("aod").textContent =
        Number(data.aod).toFixed(0);


    // ================= EXTRA CARDS =================

    document.getElementById("tempCard").textContent =
        data.temperature.toFixed(1) + "°C";

    document.getElementById("pressureCard").textContent =
        Math.round(data.pressure) + " Pa";

    document.getElementById("windCard").textContent =
        data.wind.toFixed(2) + " m/s";

    document.getElementById("dewPointCard").textContent =
        "--";


    // ================= HEALTH =================

    document.getElementById("healthMessage").textContent =
        getHealthMessage(aqi);


    // ================= MAP =================

    marker.setPopupContent(

        "<b>Delhi</b><br>AQI : " + aqi

    );

}
/* ==========================================================
   FORECAST CHART
========================================================== */

const ctx = document.getElementById("forecastChart");

let forecastChart = new Chart(ctx, {

    type: "line",

    data: {

        labels: [
            "Today",
            "+1 Day",
            "+2 Day",
            "+3 Day",
            "+4 Day",
            "+5 Day",
            "+6 Day"
        ],

        datasets: [{

            label: "Predicted AQI",

            data: [0, 0, 0, 0, 0, 0, 0],

            borderColor: "#00d4ff",

            backgroundColor: "rgba(0,212,255,0.15)",

            borderWidth: 3,

            fill: true,

            tension: 0.4,

            pointRadius: 5

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        plugins: {

            legend: {

                labels: {

                    color: "white"

                }

            }

        },

        scales: {

            x: {

                ticks: {

                    color: "white"

                }

            },

            y: {

                beginAtZero: true,

                ticks: {

                    color: "white"

                }

            }

        }

    }

});


/* ==========================================================
   UPDATE FORECAST
========================================================== */

function updateForecast(aqi){

    let values=[];

    for(let i=0;i<7;i++){

        let random=Math.floor(Math.random()*30)-15;

        values.push(

            Math.max(20,aqi+random)

        );

    }

    forecastChart.data.datasets[0].data=values;

    forecastChart.update();

}


/* ==========================================================
   INITIALIZE DASHBOARD
========================================================== */

async function initializeDashboard(){

    await fetchAQI();

    try{

        const response=await fetch(API_URL);

        const data=await response.json();

        updateForecast(Math.round(data.aqi));

    }

    catch(err){

        console.error(err);

    }

}


/* ==========================================================
   AUTO REFRESH
========================================================== */

setInterval(async()=>{

    console.log("Refreshing AQI...");

    await fetchAQI();

},300000);


/* ==========================================================
   PAGE LOAD
========================================================== */

window.addEventListener("load",()=>{

    initializeDashboard();

});


console.log("Forecast Ready");
/* ==========================================================
   AQI ANIMATION
========================================================== */

function animateAQI(target){

    const element = document.getElementById("aqiValue");

    if(!element) return;

    let current = 0;

    const step = Math.max(1, Math.ceil(target / 80));

    const timer = setInterval(() => {

        current += step;

        if(current >= target){

            current = target;

            clearInterval(timer);

        }

        element.textContent = current;

    },15);

}


/* ==========================================================
   SEARCH BOX
========================================================== */

const searchBox = document.getElementById("searchBox");

if(searchBox){

    searchBox.addEventListener("keydown",function(e){

        if(e.key !== "Enter") return;

        const city = searchBox.value.trim();

        if(city === "") return;

        alert(
            "City search will be added in the next version.\n\nCurrently showing Delhi."
        );

    });

}


/* ==========================================================
   CONNECTION TEST
========================================================== */

async function testConnection(){

    try{

        const response = await fetch(API_URL);

        if(!response.ok){

            throw new Error("API Not Reachable");

        }

        const data = await response.json();

        console.log("======================================");

        console.log("Backend Connected Successfully");

        console.table(data);

        console.log("======================================");

        animateAQI(Math.round(data.aqi));

    }

    catch(error){

        console.error("Backend Connection Failed");

        console.error(error);

    }

}

testConnection();


/* ==========================================================
   WINDOW LOADED
========================================================== */

window.addEventListener("load",()=>{

    document.body.style.opacity="1";

});


/* ==========================================================
   FINISHED
========================================================== */

console.log("======================================");

console.log("ISRO AQI Dashboard Ready");

console.log("Waiting for Live AQI...");

console.log("======================================");