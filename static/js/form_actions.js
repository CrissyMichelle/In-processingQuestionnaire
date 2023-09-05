/* Link arrival date with report date */
const arrivalDateTimeInput = document.getElementById('datetime');
const reportDateInput = document.getElementById('report');

const holidayMons = [[2023, 10,9], [2023, 11,13], [2023, 12,25]]

function isHoliday(dateArray, holidayArray) {
    for (const holiday of holidayArray) {
        if (dateArray[0]===holiday[0] && dateArray[1]===holiday[1] && dateArray[2]===holiday[2]) {
            return true;
        }
    }
    return false;
}

function getNextMonday(date = new Date()) {
    const dateCopy = new Date(date.getTime());

    const nextMonday = new Date(
        dateCopy.setDate(
            dateCopy.getDate() + ((7 - dateCopy.getDay() + 1) % 7 || 7),
        ),
    );

    return nextMonday;    
}

arrivalDateTimeInput.addEventListener('change', () => {
    //Grab the selected arrival datetimegroup and put into array as [YYYY, MM, DD]
    const arrivalDateTime = new Date(arrivalDateTimeInput.value);
    const arrivalDate = [arrivalDateTime.getFullYear(), arrivalDateTime.getMonth() + 1, arrivalDateTime.getDate()];

    //Set the report date to the following Monday and accommodate WTForms date format
    let nextReport = determineReport(arrivalDate);
    reportDateInput.value = formatDate(nextReport);
});

function determineReport(arrivalDate) {
    const arrivalDateTime = new Date(arrivalDate[0], arrivalDate[1] - 1, arrivalDate[2]);
    let nextMonday = getNextMonday(arrivalDateTime);

    let nextReportDate = [nextMonday.getFullYear(), nextMonday.getMonth() + 1, nextMonday.getDate()];
    // Check if selected report date is a holiday
    if (isHoliday(nextReportDate, holidayMons)) {
        nextMonday.setDate(nextMonday.getDate() + 1); //Move the report date to Tuesday
        nextReportDate = [nextMonday.getFullYear(), nextMonday.getMonth() + 1, nextMonday.getDate()];
    }

    return nextReportDate;
}

function formatDate(dateArray) {
    const [year, month, day] = dateArray;
    const formattedDate = `${year}-${month.toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;

    return formattedDate;
}

/* Link first and last name with initials */
const f_nameInput = document.getElementById('f_name');
const l_nameInput = document.getElementById('l_name');


function validateInitials(value) {
    return value.toUpperCase() === userInitials;
}

/* Apply the initials validator to every relevant field in the questionnaire form */
function addInitialsValidator(inputId) {
    const inputElement = document.getElementById(inputId);
    inputElement.addEventListener('input', () => {
        const f_initial = f_nameInput.value.charAt(0);
        const l_initial = l_nameInput.value.charAt(0);
        const userInitials = (f_initial + l_initial).toUpperCase();

        const isValid = inputElement.value.toUpperCase() === userInitials;
    
        inputElement.setCustomValidity(isValid ?
            '' : 'Invalid initials. Please enter two capital letters matching your first and last initials.');
    });
}

['tele_recall', 'in_proc_hours','new_pt','uniform','transpo',
'orders','da31','pov','flight','mypay', 'tdy','gtc','tla','hotels'].forEach(addInitialsValidator);

// implement "auto dashing" to phone number fields
document.addEventListener("DOMContentLoaded", () => {
    let phInput = document.getElementById("telephone");

    phInput.addEventListener("input", (e) => {
        let value = e.target.value.replace(/[^\d]/g, ""); // removes all non-digits

        if (value.length > 3 && value.length <= 6) {
            value = value.slice(0, 3) + "-" + value.slice(3);
        } else if (value.length > 6) {
            value = value.slice(0, 3) + "-" + value.slice(3,6) + "-" + value.slice(6, 10);
        }
        e.target.value = value;
    });
});