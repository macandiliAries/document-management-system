const ADMIN = (($) => {

    const userTable = $('#userTable');

    const tableCols = [
        {
            title: 'Username', className: 'text-center', data: 'username', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Full Name', className: 'text-center full_name', data: 'full_name', render: $.fn.dataTable.render.text()
        },
        {
            title: 'User Role', className: 'text-center', data: 'user_type', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Email Address', className: 'text-center', data: 'email', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Address', className: 'text-center', data: 'address', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Contact Number', className: 'text-center', data: 'contact_num', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Actions', className: 'text-center', render: (aData, oType, oRow) => {
                if (COMMON_ADMIN.currentUserType === 'Admin') {
                    return `
                        <button data-id="${oRow.id}" class="btn btn-sm btn-warning user-tbl-action" data-method="resetUserPassword"><i class="fa-solid fa-arrow-rotate-left"></i></button>
                    `;
                }

                // COMMON_ADMIN.currentUserType === 'Super Admin'
                return `
                    <button data-id="${oRow.id}" class="btn btn-sm btn-info user-tbl-action" data-method="editUser"><i class="fa-solid fa-pen-to-square"></i></button>
                    <button data-id="${oRow.id}" class="btn btn-sm btn-${(oRow.status === 'active') ? 'danger': 'success'} user-tbl-action" data-method="${(oRow.status === 'active') ? 'de': 're'}activateUser"><i class="fa-solid fa-user${(oRow.status === 'active') ? '-slash': ''}"></i></button>
                    <button data-id="${oRow.id}" class="btn btn-sm btn-warning user-tbl-action" data-method="resetUserPassword"><i class="fa-solid fa-arrow-rotate-left"></i></button>
                `;
            }
        },
    ];

    const validationRules = {
        submitHandler: () => { createUser('form[name="addUserForm"]') },
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
            },
            password        : {
                required  : true,
                minlength : 4
            },
            confirmPassword : {
                minlength : 4,
                equalTo   : '[name="password"]'
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
            },
            password        : {
                required  : 'Please enter a password.',
                minlength : $.validator.format('Please enter at least {0} characters for the password.')
            },
            confirmPassword : {
                minlength : $.validator.format('Please enter at least {0} characters for the password.'),
                equalTo   : 'Passwords do not match.'
            }
        }
    };

    const initialize = () => {
        initializeFormValidations();
        const initialUsers = $('input[name="users"]');
        initializeDataTable(JSON.parse(JSON.stringify(initialUsers.data('value'))));
        initialUsers.remove();
        setEventHandlers();
    };

    const initializeFormValidations = () => {
        // Only Super Admins can create new users.
        if (COMMON_ADMIN.currentUserType === 'Super Admin') {
            $('form[name="addUserForm"]').validate(validationRules);
        }
    };

    const initializeDataTable = async (users = []) => {
        if (users.length === 0) {
            // Get all users on the backend via Fetch API.
            users = await executeRequest({
                endpoint : '/users',
                method   : 'GET'
            });
        }

        // Remove the currently logged-in user from the response data.
        users = users.filter(userData => userData.id !== COMMON_ADMIN.currentUserId);

        const columnDefs = [
            { orderable  : false, targets: [2, 3, 4, 5, 6] },
            { searchable : false, targets: [6] }
        ];

        loadTable(userTable, users, tableCols, columnDefs, true, function () {
            const userRoleCol = this.api().column(2);
            const userRoles = [...new Set($(userRoleCol.data()))].sort(); // Get unique user roles.

            let selectDropdown = $('<select></select>')
                .addClass('custom-select')
                .append('<option value="All">User Role (Show All)</option>');

            userRoles.forEach((userType) => {
                selectDropdown.append(`<option value="${userType}">${userType}</option>`);
            });

            selectDropdown.on('change', function() {
                const optionValue = $(this).val();
                if (optionValue === 'All') {
                    return userRoleCol.search('').draw();
                }
                userRoleCol.search(`^${optionValue}$`, true, false).draw();
            });

            $(userRoleCol.header()).html(selectDropdown);
        });
    };

    const setEventHandlers = () => {
        $(document).on('click', '.addUser', () => {
            $('#addUserModal').modal('show');
        });

        $(document).on('click', '.user-tbl-action:not([data-method="editUser"])', async function () {
            const userId =  $(this).data('id');
            const userFullName = $(this).closest('tr').find('td.full_name').text();
            const possessive = (userFullName.slice(-1) === 's') ? '\'' : '\'s';
            const method = $(this).data('method');
            const messages = {
                reactivateUser    : {
                    alertTitle    : 'Reactivate Account',
                    alertText     : `Are you sure you want to reactivate ${userFullName + possessive} account?`
                },
                deactivateUser    : {
                    alertTitle    : 'Deactivate Account',
                    alertText     : `Are you sure you want to deactivate ${userFullName + possessive} account?`
                },
                resetUserPassword : {
                    alertTitle    : 'Reset Password',
                    alertText     : `Are you sure you want to reset the password for ${userFullName + possessive} account?`
                }
            };

            displayConfirm(messages[method].alertTitle, messages[method].alertText, async () => {
                const fetchProps = {
                    endpoint : `/users/${userId}`,
                    method   : 'PATCH',
                    body     : {
                        action : method
                    }
                };
                return await executeRequest(fetchProps);
            }).then((result) => {
                if (result.isConfirmed === true) {
                    const response = result.value;
                    displayAlert(response.result, response.title, response.message, () => {
                        if (response.result === true) {
                            initializeDataTable();
                        }
                    });
                }
            });
        });
    };

    const createUser = async (formSelector) => {
        const requestData = getRequestData(formSelector);
        toggleInputs('disable');
        toggleSpinner('show');

        const response = await executeRequest({
            endpoint : '/users',
            method   : 'POST',
            body     : requestData
        });

        displayAlert(response.result, response.title, response.message, () => {
            toggleInputs('enable');
            toggleSpinner('hide');
            if (response.result === true) {
                initializeDataTable();
                $(formSelector).closest('.modal').modal('hide');
            }
        });
    };

    return {
        initialize          : initialize,
        initializeDataTable : initializeDataTable
    }
})(jQuery);

$(() => {
    ADMIN.initialize();
});