function change_ID() {
 
    var darkLayer = document.createElement('div');
    darkLayer.id = 'shadow'; 
    document.body.appendChild(darkLayer);

    var modalWin = document.getElementById('block_change_ID'); 
    modalWin.style.display = 'block'; 

    darkLayer.onclick = function () {  
        darkLayer.parentNode.removeChild(darkLayer); 
        modalWin.style.display = 'none'; 
        return false;
    };
}

function change_name() {
 
    var darkLayer = document.createElement('div');
    darkLayer.id = 'shadow'; 
    document.body.appendChild(darkLayer);

    var modalWin = document.getElementById('block_change_name');
    modalWin.style.display = 'block'; 

    darkLayer.onclick = function () {  
        darkLayer.parentNode.removeChild(darkLayer); 
        modalWin.style.display = 'none'; 
        return false;
    };
}

function delete_emp() {
 
    var darkLayer = document.createElement('div');
    darkLayer.id = 'shadow'; 
    document.body.appendChild(darkLayer);

    var modalWin = document.getElementById('block_delete_emp');   
    modalWin.style.display = 'block'; 

    darkLayer.onclick = function () {  
        darkLayer.parentNode.removeChild(darkLayer); 
        modalWin.style.display = 'none'; 
        return false;
    };
}

function update_key() {
 
    var darkLayer = document.createElement('div');
    darkLayer.id = 'shadow'; 
    document.body.appendChild(darkLayer);

    var modalWin = document.getElementById('block_update_key');   
    modalWin.style.display = 'block'; 

    darkLayer.onclick = function () {  
        darkLayer.parentNode.removeChild(darkLayer); 
        modalWin.style.display = 'none'; 
        return false;
    };
}
function update_roli() {
 
    var darkLayer = document.createElement('div');
    darkLayer.id = 'shadow'; 
    document.body.appendChild(darkLayer);

    var modalWin = document.getElementById('block_update_roli');   
    modalWin.style.display = 'block'; 

    darkLayer.onclick = function () {  
        darkLayer.parentNode.removeChild(darkLayer); 
        modalWin.style.display = 'none'; 
        return false;
    };
}


function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
}