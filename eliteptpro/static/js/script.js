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

    // initialize the holiday datepicker
    let datepicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepicker, {
        disableWeekends: true,
        format: "dd, mmm, yyyy",
        autoClose: true,
    })

    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);

    let form = document.getElementById("pt-form");
    if (form !== null) {

        // pt session datepicker initialization
        getHolidays()
            .then((holidays) => {
                // initialize the materialize datepicker
                let datepicker = document.querySelectorAll('.datepicker');
                M.Datepicker.init(datepicker, {
                    disableWeekends: true,
                    format: "dd, mmm, yyyy",
                    autoClose: true,
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

        getTimes()
    }
})





function getHolidays() {
    /**
     * sends request to backend to retrieve list of holidays for selected trainer
     * formats returned array to a format accepted by datepicker for use in datepicker
     */
    return new Promise((resolve, reject) => {
        // add event listener on dropdown selection change
        let trainerSelect = document.getElementById("trainer_name");
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

function getTimes() {
    /**
     * sends request to backend to retrieve list of times booked on specific date for selected trainer
     * and disable option in dropdown list
     */
    let dateSelect = document.getElementById("date");
    let selectbox = document.getElementById("time");
    // add event listener on ddatepicker selection change
    dateSelect.addEventListener("change", function () {
        let selectedDate = this.value;
        let selectedTrainer = document.getElementById("trainer_name").value;
        // send request to flask backend to retrieve times from db
        let xhr = new XMLHttpRequest();
        xhr.open("POST", "/search_times", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({
            "selected_date": selectedDate,
            "selected_trainer": selectedTrainer
        }));
        // response from backend
        xhr.onload = function () {
            let selectbox = document.getElementById("time");
            let response = JSON.parse(xhr.responseText);
            let times = response.times;
            // create array of potential times 
            let openingHours = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00"];
            // set a default selected option
            let defaultOption = document.createElement("option");
            defaultOption.value = "";
            defaultOption.text = "Select a time";
            defaultOption.selected = true; // Set as default selected option
            defaultOption.disabled = true; // Disable the default option
            selectbox.appendChild(defaultOption);
            // iterate over openingHours array and create an option for the dropdown
            for (let hour of openingHours) {
                let option = document.createElement("option");
                option.value = hour;
                option.text = hour;
                // if hour is in array of times retrieved from db add disabled attribute
                if (times.includes(hour)) {
                    option.disabled = true;
                }

                selectbox.appendChild(option);
            }
            // initialize dropdown
            M.FormSelect.init(selectbox);
        }

    })
}