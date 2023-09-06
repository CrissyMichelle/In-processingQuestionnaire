$(document).ready(function() {
    //Attach click event to elements with the class "like-button"
    $('.like-button').click(function(e) {
        e.preventDefault();

        const messageId = $(this).data('message-id');
        const counterElement = $(`#like-counter-${messageId}`);
        const currentCount = parseInt(counterElement.text());

        $.ajax({
            type: "POST",
            url: `/messages/${messageId}/like`,
            success: (response) => {
                if(response.status === "success" && response.action === "increment") {
                    // Increment like-counter, toggle thumbs up icon
                    counterElement.text(currentCount + 1);
                    $(`#like-button-${messageId}`).toggleClass('btn-primary btn-secondary');
                } else if (response.action === "decrement") {
                    counterElement.text(currentCount - 1);
                    $(`#like-button-${messageId}`).toggleClass('btn-primary btn-secondary');
                } else {
                    // Handle failure
                    alert(response.message);
                }
            },
            error: (error) => {
                alert('An error occured');
            }
        });
    });
});