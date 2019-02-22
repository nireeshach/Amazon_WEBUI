// This code is used to render a HTML table from uploaded CSV file using d3.js
window.totalResults = 0

var tabulate = function (
    data, columns, tablediv, id) {
    window.totalResults = data.length;
    var table = d3.select(tablediv).append('table')
    table.attr("class", "table table-striped table-bordered table-responsive")
    table.attr("id", id)
    table.attr("style", "width: auto")

    var thead = table.append('thead')
    var tbody = table.append('tbody')

    // append the header row
    thead.append('tr')
        .selectAll('th')
        .data(columns).enter()
        .append('th')
        .text(function (column) { return column; });

    // create a row for each object in the data
    var rows = tbody.selectAll('tr')
        .data(data)
        .enter()
        .append('tr');

    // create a cell in each row for each column
    var cells = rows.selectAll('td')
        .data(function (row) {
            return columns.map(function (column) {
                return { column: column, value: row[column] };
            });
        })
        .enter()
        .append('td')
        .text(function (d) { return d.value; });

    return table;
}
