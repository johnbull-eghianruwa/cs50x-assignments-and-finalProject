document.addEventListener('DOMContentLoaded', function () {

    ////////////////////////////////////////////////////////////////
    /////// Add event listeners to your dropdown elements //////////
    ///////////////////////////////////////////////////////////////
    var dropdowns = document.querySelector('.dropdown');

    dropdowns.addEventListener('mouseover', function () {
        this.querySelector('.dropdown-content').style.display = 'block';
    });

    dropdowns.addEventListener('mouseout', function () {
        this.querySelector('.dropdown-content').style.display = 'none';
    });
});