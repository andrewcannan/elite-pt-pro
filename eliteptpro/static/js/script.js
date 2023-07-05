document.addEventListener('DOMContentLoaded', function () {
    // sidenav initialization
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {
        closeOnClick: true,
        edge: 'right'
    });

    // slideshow initialization
    let slider = document.querySelectorAll('.slider');
    M.Slider.init(slider,{
        indicators: false
    });

    // dropdown select initilization
    let dropdown = document.querySelectorAll('select');
    M.FormSelect.init(dropdown);


    let datepicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepicker, {
        disableWeekends: true,
        format: "dd, mmm, yyyy"
        });

});
