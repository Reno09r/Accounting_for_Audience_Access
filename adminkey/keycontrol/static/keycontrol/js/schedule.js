document.querySelectorAll('.day-button').forEach(function(button) {
    button.addEventListener('click', function() {
        var dayOfWeek = this.innerText.trim();
        filterByDay(dayOfWeek);
    });
});

function filterByDay(day) {
    fetch(`/schedule/?day_of_week=${encodeURIComponent(day)}`)
        .then(response => response.json())
        .then(data => {
            updateTable(data.rows);
        })
        .catch(error => console.error('Error:', error));
}

function updateTable(rows) {
    var table = document.getElementById('info');

    while (table.rows.length > 1) {
        table.deleteRow(1);
    }

    rows.forEach(function (row) {
        var newRow = table.insertRow(-1);

        var cell1 = newRow.insertCell(0);
        var cell2 = newRow.insertCell(1);
        var cell3 = newRow.insertCell(2);
        var cell4 = newRow.insertCell(3);
        var cell5 = newRow.insertCell(4);
        var cell6 = newRow.insertCell(5);

        cell1.innerHTML = `<input type="checkbox" data-row-id="${row.id}">`;
        cell2.innerHTML = row.full_name;
        cell3.innerHTML = row.key;
        cell4.innerHTML = row.start_time;
        cell5.innerHTML = row.end_time;
        cell6.innerHTML = row.day_of_week;
    });
}