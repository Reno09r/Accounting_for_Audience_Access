document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('.search_img').addEventListener('click', function () {
        var searchAdminForm = document.getElementById('SearchAdminForm');
        if (searchAdminForm) {
            searchAdminForm.submit();
        } else {
            document.getElementById('searchForm').submit();
        }
    });
});