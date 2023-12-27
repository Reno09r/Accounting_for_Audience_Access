function ReturnKeys(csrfToken) {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var selectedIds = Array.from(checkboxes).map(function(checkbox) {
        return checkbox.dataset.rowId;
    });

    fetch('/mark_returned/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')  
        },
        body: JSON.stringify({
            'action': 'mark_returned',
            'selected_ids': selectedIds
        })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        location.reload(true)
    });
}

function DeleteSchedule(csrfToken) {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var selectedIds = Array.from(checkboxes).map(function(checkbox) {
        return checkbox.dataset.rowId;
    });

    fetch('/mark_delete/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')  
        },
        body: JSON.stringify({
            'action': 'mark_delete',
            'selected_ids': selectedIds
        })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        location.reload(true)
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}