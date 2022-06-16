const LOGIN = (() => {

    const initialize = () => {
        setEventHandlers();
    }

    const setEventHandlers = () => {
        $(document).on('click', '#doLogin', () => {
            const validateCreds = validateLoginInputs();
            if (validateCreds.result === false) {
                displayAlert(false, validateCreds.title, validateCreds.message);
                return false;
            }

            submitData();
        });

        // If the ENTER key has been pressed when inside any input element of the login form, submit data.
        $(document).find('form[name="loginForm"] input').on('keypress', (event) => {
            const keyCode = event.keyCode || event.which;
            if (keyCode === 13) {
                $('#doLogin').trigger('click');
            }
        });
    }

    const validateLoginInputs = () => {
        // Check if the username has a value or not.
        if (isEmpty($('input[name="username"]').val()) === true) {
            return {
                result  : false,
                title   : 'Invalid Credential',
                message : 'Please enter your username.'
            }
        }

        // Check if the password has a value or not.
        if (isEmpty($('input[name="password"]').val()) === true) {
            return {
                result  : false,
                title   : 'Invalid Credential',
                message : 'Please enter your password.'
            }
        }

        return {
            result : true
        };
    }

    const submitData = async () => {
        const requestData = getRequestData();
        toggleInputs('disable');
        toggleSpinner('show');

        const response = await executeRequest({
            endpoint : '/login',
            method   : 'POST',
            body     : requestData
        });

        if (response.result === true) {
            location.reload();
            return true;
        }

        displayAlert(response.result, response.title, response.message, () => {
            toggleInputs('enable');
            toggleSpinner('hide');
        });
    }

    const getRequestData = () => {
        let formData = (Object.fromEntries(new FormData($('form[name="loginForm"]')[0]).entries()));
        Object.keys(formData).map((key) => {
            // Trim whitespaces.
            formData[key] = $.trim(formData[key]);
        });
        return formData;
    }

    return {
        initialize : initialize
    }
})();

$(() => {
    LOGIN.initialize();
});