document.getElementById("endpoint-form").addEventListener("submit", (e) => {
    console.log("Form submitted? Check.");

    e.preventDefault();

    let endPointField = document.querySelector("[name='destination']");
    let csrfTokenField = document.querySelector("[name='csrf_token']");
    let end_point = endPointField.value;
    let csrf_token = csrfTokenField.value

    //Prepare data for async API call
    let formData = new FormData();
    formData.append("destination", end_point);
    formData.append("csrf_token", csrf_token);
    //AJAX request to server, indicated by XML Http header
    fetch("/resources", {
        method: "POST",
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            let url = `/directions?origin=Lyman Gate, HI&destination=${end_point}&mode=DRIVING`;
            window.location.href = url;
        } else {
            alert("Error: " + data.error);
        }
    }).catch(error => console.error("Oops, error!", error));    
})