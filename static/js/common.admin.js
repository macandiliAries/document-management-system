const COMMON_ADMIN = (($, currentPage) => {
    const currentUserId = parseInt($('input#currentUser').val());

    const currentUserType = $('input#currentUserType').val();

    let validationRules = {
        editUser       : {
            submitHandler: () => { submitData('form[name="editUserForm"]') },
            errorElement: 'small',
            errorPlacement: (errorLabel, elementToValidate) => {
                errorLabel.addClass('mt-n2 mb-n2 form-text text-danger text-right');
                elementToValidate.closest('div.form-group').append(errorLabel);
            },
            rules: {
                full_name       : {
                    required  : true,
                    minlength : 4,
                    maxlength : 100
                },
                email           : {
                    required : true,
                    email    : true
                },
                address         : {
                    required  : true,
                    minlength : 4,
                    maxlength : 100
                },
                contact_num     : {
                    required  : true,
                    digits    : true,
                    maxlength : 13
                },
                user_type       : {
                    required       : true,
                    allowedValues  : 'Super Admin, Admin'
                },
                username        : {
                    required  : true,
                    minlength : 4,
                    maxlength : 50
                }
            },
            messages: {
                full_name       : {
                    required  : 'Please enter full name.',
                    minlength : $.validator.format('Please enter at least {0} characters for the full name.'),
                    maxlength : $.validator.format('Maximum of {0} characters are only allowed for the full name.')
                },
                email           : {
                    required  : 'Please enter an email address.',
                    email     : 'Please enter a valid email.'
                },
                address         : {
                    required  : 'Please enter an address.',
                    minlength : $.validator.format('Please enter at least {0} characters for the address.'),
                    maxlength : $.validator.format('Maximum of {0} characters are only allowed for the address.')
                },
                contact_num     : {
                    required  : 'Please enter contact number.',
                    maxlength : $.validator.format('Maximum of {0} characters are only allowed for the contact number.')
                },
                user_type       : {
                    required  : 'Please enter a user role.'
                },
                username        : {
                    required  : 'Please enter a username.',
                    minlength : $.validator.format('Please enter at least {0} characters for the username.'),
                    maxlength : $.validator.format('Maximum of {0} characters are only allowed for the username.')
                }
            }
        },
        changePassword : {
            submitHandler: () => { submitData('form[name="changePasswordForm"]') },
            errorElement: 'small',
            errorPlacement: (errorLabel, elementToValidate) => {
                errorLabel.addClass('mt-n2 mb-n2 form-text text-danger text-right');
                elementToValidate.closest('div.form-group').append(errorLabel);
            },
            rules: {
                oldPassword        : {
                    required  : true,
                },
                newPassword        : {
                    required  : true,
                    minlength : 4,
                },
                confirmNewPassword : {
                    minlength : 4,
                    equalTo   : '[name="newPassword"]'
                }
            },
            messages: {
                oldPassword        : {
                    required  : 'Please enter your old password.',
                },
                newPassword        : {
                    required  : 'Please enter your new password.',
                    minlength : $.validator.format('Please enter at least {0} characters for your new password.'),
                },
                confirmNewPassword : {
                    required  : 'Please confirm your new password.',
                    minlength : $.validator.format('Please enter at least {0} characters for your new password.'),
                    equalTo   : 'Passwords do not match.'
                }
            }
        }
    };

    const initialize = () => {
        initializeFormValidation();
        setEventHandlers();
    };

    const initializeFormValidation = () => {
        // Only Super Admins can change user role of existing users.
        if (currentUserType === 'Admin') {
            delete validationRules.editUser.rules.user_type;
            delete validationRules.editUser.messages.user_type;
        }
        $('form[name="editUserForm"]').validate(validationRules.editUser);
        $('form[name="changePasswordForm"]').validate(validationRules.changePassword);
    };

    const setEventHandlers = () => {
        $(document).on('click', '[data-method="editUser"]', async function () {
            const editUserModal = $('#editUserModal');
            const userDetails = await getUserDetails($(this).data('id'));
            $.each(Object.keys(userDetails), (index, keyName) => {
                const value = userDetails[keyName];
                if (keyName === 'user_type') {
                    editUserModal.find(`select[name="${keyName}"] option[value="${value}"]`).prop('selected', true);
                    return true; // Proceed to the next iteration.
                }
                editUserModal.find(`input[name="${keyName}"]`).val(value);
            });
            editUserModal.find('input[name="action"]').val('updateUserDetails');
            editUserModal.modal('show');
        });

        $(document).on('click', '[data-method="changePassword"]', () => {
            const changePassModal = $('#changePassModal');
            changePassModal.find('input[name="id"]').val(currentUserId);
            changePassModal.find('input[name="action"]').val('updatePassword');
            changePassModal.modal('show');
        });
    };

    const getUserDetails = async (userId) => {
        return await executeRequest({
            endpoint : `/users/${userId}`,
            method   : 'GET'
        });
    };

    const submitData = async (formSelector) => {
        const requestData = getRequestData(formSelector);
        toggleInputs('disable');
        toggleSpinner('show');

        const userId = parseInt(requestData.id, 10);
        delete requestData.id;

        const response = await executeRequest({
            endpoint : `/users/${userId}`,
            method   : 'PATCH',
            body     : requestData
        });

        displayAlert(response.result, response.title, response.message, () => {
            toggleInputs('enable');
            toggleSpinner('hide');
            if (response.result === true) {
                $(formSelector).closest('.modal').modal('hide');

                // Check if the details of the currently logged-in user have been updated.
                if (requestData.action === 'updateUserDetails' && userId === currentUserId) {
                    // If so, update the full name label on the nav header.
                    $('#fullNameLabel').text(requestData.full_name);
                }

                if (currentPage === '/admin') {
                    ADMIN.initializeDataTable();
                }
            }
        });
    };

    return { 
        initialize,
        currentUserId,
        getUserDetails,
        currentUserType
    }
})(jQuery, window.location.pathname);

$(() => {
    COMMON_ADMIN.initialize();
});