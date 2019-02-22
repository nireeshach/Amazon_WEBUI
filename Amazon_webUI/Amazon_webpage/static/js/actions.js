$(document).ready(function () {


    $('#get_url').on("click", function (event) {


        event.preventDefault();
        event.stopPropagation();

        // Hiding all alerts
        $(".alert").hide()

        $('#relevantTable').remove()
        $('#irrelevantTable').remove()
        document.getElementById('stars').innerHTML = "";

        // Removing data table, when clicked on submit

        $.ajax({
            url: "/getURL",
            type: 'POST',
            data: JSON.stringify({ "url": document.getElementById('url').value }),
            dataType: 'json',
            contentType: 'application/json',
            success: function (data, textStatus, jqXHR) {

                reviewResults(
                    data.relevant_results,
                    "#relevantreviews",
                    "#testcontent",
                );
                irrelevantresults(data.irrelevant_results,
                    "#irrelevantreviews",
                    "#reviewcontent"
                );
                $("#rat").text("Adjusted Star Rating: " + data.rating + " out of 5")
                document.getElementById("stars").innerHTML = getStars(data.rating);
                $("#inwords").text("Amazon Original Rating: " + data.product_rating + " out of 5")
                document.getElementById("delta").innerHTML = "Delta : " + getdelta(data.rating, data.product_rating)
                if (data.rating > data.product_rating) {
                    $(".arrow-up-red").show();

                };
                if (data.rating < data.product_rating) {
                    $(".arrow-down-green").show();

                };

                document.getElementById('url').value = "";

                $.LoadingOverlay("hide");
                // $("#url).display();
                $("#main-form").toggle();


                $("#success-alert").text(
                    "Success! " + data.message
                ).show()

            },

            error: function (XMLHttpRequest) {
                $.LoadingOverlay("hide");
                $("#failed-alert").text(
                    "Failed! " + XMLHttpRequest.responseJSON.message
                ).show()
            },
            beforeSend: function () {
                $.LoadingOverlay("show");
            },
        });
    });
});
