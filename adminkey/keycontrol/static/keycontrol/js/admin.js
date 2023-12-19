function showModalWin() {

    var darkLayer = document.createElement('div');
    darkLayer.id = 'shadow'; 
    document.body.appendChild(darkLayer); 

    var modalWin = document.getElementById('popupWin');
    modalWin.style.display = 'block';

    darkLayer.onclick = function () {  
        darkLayer.parentNode.removeChild(darkLayer); 
        modalWin.style.display = 'none'; 
        return false;
    };
}

document.getElementById('minusButton').addEventListener('click', function() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var data = {
        'action': 'mark_returned',
        'selected_ids': Array.from(checkboxes).map(function(checkbox) {
            return checkbox.closest('tr').dataset.rowId;
        })
    };

    fetch('/mark_returned/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(data)
    }).then(function(response) {
        console.log(response);
    });
});