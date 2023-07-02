document.addEventListener('DOMContentLoaded', function () {
    // sidenav initialization
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {
        closeOnClick: true,
        edge: 'right'
    });

    let slider = document.querySelectorAll('.slider');
    M.Slider.init(slider,{
        indicators: false
    });
});
