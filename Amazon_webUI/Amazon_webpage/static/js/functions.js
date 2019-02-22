// Function to render relevant reviews as HTML table

function reviewResults(data, cont, displayid) {
    var data = data.slice(0, 10),
        // Getting column names from first row
        columns = d3.keys(data[0]);

    // Calling tabulate from render_table.js
    window.resultsTable = tabulate(data, columns, cont, "relevantTable")
    $(displayid).show()
}

function irrelevantresults(data, cont, displayid) {
    var data = data.slice(0, 10),
        // Getting column names from first row
        columns = d3.keys(data[0]);

    // Calling tabulate from render_table.js
    window.resultsTable = tabulate(data, columns, cont, "irrelevantTable")
    $(displayid).show()
}


function getStars(rating) {

    // Round to nearest half
    rating = Math.round(rating * 2) / 2;
    let output = [];

    // Append all the filled whole stars
    for (var i = rating; i >= 1; i--)
        output.push('<i class="fa fa-star" aria-hidden="true" style="color: gold;"></i>&nbsp;');

    // If there is a half a star, append it
    if (i == .5) output.push('<i class="fa fa-star-half-o" aria-hidden="true" style="color: gold;"></i>&nbsp;');

    // Fill the empty stars
    for (let i = (5 - rating); i >= 1; i--)
        output.push('<i class="fa fa-star-o" aria-hidden="true" style="color: gold;"></i>&nbsp;');

    return output.join('');

}

function getdelta(rating, productrating) {

    var v1 = rating;
    var v2 = productrating;

    delta = v2 - v1;

    return delta.toFixed(2)

}
