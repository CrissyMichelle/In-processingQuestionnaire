// implement "auto dashing" to phone number fields
document.addEventListener("DOMContentLoaded", () => {
    let phInput = document.getElementById("telephone");

    phInput.addEventListener("input", (e) => {
        let value = e.target.value.replace(/[^\d]/g, ""); // removes all non-digits

        if (value.length > 3 && value.length <= 6) {
            value = value.slice(0, 3) + "-" + value.slice(3);
        } else if (value.length > 6) {
            value = value.slice(0, 3) + "-" + value.slice(3,6) + "-" + value.slice(6, 10);
        }
        e.target.value = value;
    });
});