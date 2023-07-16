document.addEventListener('DOMContentLoaded', function () {
    // sidenav initialization
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav, {
        closeOnClick: true,
        edge: 'right'
    });

    // slideshow initialization
    let slider = document.querySelectorAll('.slider');
    M.Slider.init(slider, {
        indicators: false
    });

    // dropdown select initilization
    let dropdown = document.querySelectorAll('select');
    M.FormSelect.init(dropdown);

    // datepicker initialization
    getHolidays()
        .then((holidays) => {
            // initialize the materialize datepicker
            let datepicker = document.querySelectorAll('.datepicker');
            M.Datepicker.init(datepicker, {
                disableWeekends: true,
                format: "dd, mmm, yyyy",
                disableDayFn: (date) => {
                    // convert date to format expected by Materialize CSS (YYYY-MM-DD)
                    const year = date.getFullYear();
                    const month = String(date.getMonth() + 1).padStart(2, '0');
                    const day = String(date.getDate()).padStart(2, '0');
                    const formattedDate = `${year}-${month}-${day}`;

                    // check if the formatted date is in the holidays array
                    return holidays.includes(formattedDate);
                },
            });
        })
});

function getHolidays() {
    return new Promise((resolve, reject) => {
        // xml request to retrieve holidays for selected trainer
        let trainerSelect = document.getElementById("trainer_name");
        // add event listener on dropdown selection change
        trainerSelect.addEventListener("change", function () {
            let selectedTrainer = this.value;
            // send request to flask backend to retrieve holidays from db
            let xhr = new XMLHttpRequest();
            xhr.open("POST", "/search_holidays", true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify({
                "selected_trainer": selectedTrainer
            }));
            // response from backend
            xhr.onload = function () {
                let response = JSON.parse(xhr.responseText);
                let holidays = response.holidays;
                let formattedDates = [];
                // convert date to format expected by Materialize CSS (YYYY-MM-DD)
                for (let holiday of holidays) {
                    let date = new Date(Date.parse(holiday));
                    let year = date.getFullYear();
                    let month = String(date.getMonth() + 1).padStart(2, '0');
                    let day = String(date.getDate()).padStart(2, '0');
                    let formattedDate = `${year}-${month}-${day}`;
                    formattedDates.push(formattedDate);
                };
                resolve(formattedDates);
            };
        });
    })
};