/* Link arrival date with report date */
const arrivalDateTimeInput = document.getElementById('datetime');
const reportDateInput = document.getElementById('report');

const mondays = [[2023, 9,11], [2023, 9,18], [2023, 9,25], [2023, 10,2], [2023, 10,2],
    [2023, 10,10], [2023, 10,16], [2023, 10,23], [2023, 10,30], [2023, 11,6], [2023, 11,14],
    [2023, 11,20], [2023, 11, 27], [2023, 12,4], [2023, 12,4], [2023, 12,11], [2023, 12,18],
    [2023, 12,26]]

arrivalDateTimeInput.addEventListener('change', () => {
    //Grab the selected arrival datetimegroup and put into array as [YYYY, MM, DD]
    const arrivalDateTime = new Date(arrivalDateTimeInput.value);
    const arrivalDate = [arrivalDateTime.getFullYear(), arrivalDateTime.getMonth() + 1, arrivalDateTime.getDate()];

    //Set the report date to the following Monday and accommodate WTForms date format
    let nextReport = determineReport(arrivalDate);
    reportDateInput.value = formatDate(nextReport);
})

function determineReport(arrivalDate) {
    for (const monday of mondays) {
        if (arrivalDate[1] === monday[1] && arrivalDate[2] < monday[2]) {
            return monday;
        }
    }
    return [2027, 11, 10];
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

/* The following very non-DontRepeatYourself code inspired the above. Try and eliminate the sopping wet stuff lol.
const tele_recallInput = document.getElementById('tele_recall');
tele_recallInput.addEventListener('input', () => {
    const f_initial = f_nameInput.value.charAt(0);
    const l_initial = l_nameInput.value.charAt(0);
    const userInitials = (f_initial + l_initial).toUpperCase();

    const isValid = tele_recallInput.value.toUpperCase() === userInitials;
    
    tele_recallInput.setCustomValidity(isValid ?
        '' : 'Invalid initials. Please enter two capital letters matching your first and last initials.');
})

const in_proc_hoursInput = document.getElementById('in_proc_hours');
in_proc_hoursInput.addEventListener('input', () => {
    const f_initial = f_nameInput.value.charAt(0);
    const l_initial = l_nameInput.value.charAt(0);
    const userInitials = (f_initial + l_initial).toUpperCase();

    const isValid = in_proc_hoursInput.value.toUpperCase() === userInitials;
    
    in_proc_hoursInput.setCustomValidity(isValid ?
        '' : 'Invalid initials. Please enter two capital letters matching your first and last initials.');
})
const new_ptInput = document.getElementById('new_pt');
new_ptInput.addEventListener('input', () => {
    const f_initial = f_nameInput.value.charAt(0);
    const l_initial = l_nameInput.value.charAt(0);
    const userInitials = (f_initial + l_initial).toUpperCase();

    const isValid = new_ptInput.value.toUpperCase() === userInitials;
    
    new_ptInput.setCustomValidity(isValid ?
        '' : 'Invalid initials. Please enter two capital letters matching your first and last initials.');
})
const uniformInput = document.getElementById('uniform');
uniformInput.addEventListener('input', () => {
    const f_initial = f_nameInput.value.charAt(0);
    const l_initial = l_nameInput.value.charAt(0);
    const userInitials = (f_initial + l_initial).toUpperCase();

    const isValid = uniformInput.value.toUpperCase() === userInitials;
    
    uniformInput.setCustomValidity(isValid ?
        '' : 'Invalid initials. Please enter two capital letters matching your first and last initials.');
})
const transpoInput = document.getElementById('transpo');
transpoInput.addEventListener('input', () => {
    const f_initial = f_nameInput.value.charAt(0);
    const l_initial = l_nameInput.value.charAt(0);
    const userInitials = (f_initial + l_initial).toUpperCase();

    const isValid = transpoInput.value.toUpperCase() === userInitials;
    
    transpoInput.setCustomValidity(isValid ?
        '' : 'Invalid initials. Please enter two capital letters matching your first and last initials.');
})

const ordersInput = document.getElementById('orders');
ordersInput.addEventListener('input', () => {
    const f_initial = f_nameInput.value.charAt(0);
    const l_initial = l_nameInput.value.charAt(0);
    const userInitials = (f_initial + l_initial).toUpperCase();

    const isValid = ordersInput.value.toUpperCase() === userInitials;
    
    ordersInput.setCustomValidity(isValid ?
        '' : 'Invalid initials. Please enter two capital letters matching your first and last initials.');
})

... etc...*/
