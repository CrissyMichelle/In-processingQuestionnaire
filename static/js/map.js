let panel = document.getElementById("route-panel");
    
function initMap() {
    const service = new google.maps.DirectionsService();
    const render = new google.maps.DirectionsRenderer();
    
    let location = {lat: 21.497707099641616, lng: -158.06826180360926};
    let map = new google.maps.Map(document.getElementById("map"), {
        zoom: 11,
        center: location
    });
    let marker = new google.maps.Marker({
        position: location,
        map: map
    });
    const detailWindow = new google.maps.InfoWindow({
        content: `<h2 class="text-dark">Bldg 1020</h2>`
    });
    marker.addListener("mouseover", () => { 
        detailWindow.open(map, marker)
    })
    
    render.setMap(map);
    render.setPanel(panel);

    //Extract the API call parameters from the URL or from the get-directions form
    let urlParams = new URLSearchParams(window.location.search);
    let start = urlParams.get('origin') || document.getElementById("origin").value;
    let end = urlParams.get('destination') || document.getElementById("destination").value;
    let mode = urlParams.get('mode') || document.getElementById("travelMode").value;

    //Extract parameters from redirected URL's query arguments
    function fetchAndRender() {
        fetch(`/api/directions?origin=${start}&destination=${end}&mode=${mode}`).then((response) => response.json())
        .then((data) => {
            service.route({
                origin: data.origin,
                destination: data.destination,
                travelMode: google.maps.TravelMode[data.travelMode]
            }).then(function(response) {
                render.setDirections(response);
            }).catch(function(error) {
                console.log("Error: ", error);
            })
        });
    }


    //Render API call response immediately on page load
    fetchAndRender();

    document.getElementById("get-directions").addEventListener("submit", (e) => {
        e.preventDefault()

        //Update arguments with input from the get-directions form
        start = document.getElementById("origin").value;
        end = document.getElementById("destination").value;
        mode = document.getElementById("travelMode").value;

        fetchAndRender();
    })
}