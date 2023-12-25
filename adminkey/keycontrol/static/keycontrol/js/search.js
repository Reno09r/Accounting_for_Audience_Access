function setupFormFilter(formId, inputId, selectId) {
    var form = document.getElementById(formId);

    if (!form) {
        console.error("Form not found:", formId);
        return;
    }

    var input = form.querySelector("#" + inputId);
    var selectField = form.querySelector("#" + selectId);

    if (!input || !selectField) {
        console.error("Input or select field not found:", inputId, selectId);
        return;
    }

    input.addEventListener("input", function() {
        var options = selectField.querySelectorAll("option");
        var inputValue = input.value.toLowerCase();
        var matchFound = false;

        options.forEach(function(option, index) {
            var optionText = option.text.toLowerCase();

            if (optionText.includes(inputValue)) {
                option.style.display = "block";
                selectField.selectedIndex = index;
                matchFound = true;
            } else {
                option.style.display = "none";
            }
        });

        if (!matchFound && inputValue === "") {
            selectField.selectedIndex = 0;
        } else if (!matchFound) {
            selectField.selectedIndex = -1;
        }
    });
}
setupFormFilter("block_change_ID", "id_full_name", "id_emp_selected");
setupFormFilter("block_change_name", "id_full_name_search", "id_emp_selected");
setupFormFilter("block_delete_emp", "id_item_name", "id_item_selected");
setupFormFilter("block_update_key", "id_item_name", "id_item_selected");
setupFormFilter("block_update_roli", "id_item_name", "id_item_selected");
setupFormFilter("popupWin", "id_full_name", "id_emp_choose");
setupFormFilter("popupWin", "id_key", "id_key_choose");