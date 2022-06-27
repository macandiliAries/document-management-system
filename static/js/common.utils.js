const toggleInputs = (action) => {
    $('input, select, radio, textarea').prop('disabled', action === 'disable');
    // For Summernote-related elements, disable the wysiwyg editor.
    const summernote = $('[data-input-type="summernote"]');
    if (summernote.length > 0) {
        summernote.summernote(action);
    }
};

const toggleSpinner = (action) => {
    if (action === 'show') {
        $('.action-btn').addClass('d-none');
        $('.loading-status').removeClass('d-none');
    } else {
        $('.action-btn').removeClass('d-none');
        $('.loading-status').addClass('d-none');
    }
};

const clearInputs = (querySelector = document) => {
    $(querySelector).find('input').map((index, input) => $(input).val(''));
    $(querySelector).find('select').map((index, select) => $(select).prop('selectedIndex', 0));

    // For Summernote-related elements, clear the text contents and re-display the placeholder.
    $(querySelector).find('div[contenteditable]').map((index, contents) => $(contents).html('<p><br></p>'));
    $(querySelector).find('.note-placeholder').css('display', 'block');
};

const isEmpty = (value) => {
    return inArray($.trim(value), ['', null, undefined]) === true;
};

const getRequestData = (formSelector) => {
    let formData = (Object.fromEntries(new FormData($(formSelector)[0]).entries()));
    Object.keys(formData).map((key) => {
        // Trim whitespaces.
        formData[key] = $.trim(formData[key]);
    });

    return formData;
};

const executeRequest = async (properties) => {
    const fetchOptions = {
        method: properties.method,
        headers: {
            'Content-Type' : 'application/json'
        }
    };

    const csrfEnabledEndpoint = inArray(fetchOptions.method, ['POST', 'PATCH', 'DELETE']) === true;
    const csrfInput = $('input[name="X-CSRFToken"]');

    if (csrfEnabledEndpoint === true && isEmpty(properties.body) === false) {
        fetchOptions.headers['X-CSRFToken'] = csrfInput.val();
        fetchOptions.body = JSON.stringify(properties.body);
    }
    
    let returnData = {};
    try {
        const response = await fetch(properties.endpoint, fetchOptions);
        returnData = await response.json();

        // Refresh the CSRF token value.
        if (csrfEnabledEndpoint === true) {
            csrfInput.val(returnData.new_token);
        }
    } catch (error) {
        await displayAlert(false, 'Invalid Request', 'Connection to the server has been lost. Page will now refresh.', () => { location.reload(); });
    }

    return returnData;
};

const displayAlert = async (result, alertTitle, alertMessage, callback = () => {}) => {
    const swalAlert = Swal.fire({
        icon              : (result === false) ? 'error' : 'success',
        title             : alertTitle,
        text              : alertMessage,
        allowEscapeKey    : false,
        allowOutsideClick : false,
    }).then((result) => {
        if (result.isConfirmed === true) {
            // Remove the tabindex attribute on the Swal popup (to allow copying Swal text contents).
            $(Swal.getContainer()).children().first().removeAttr('tabindex');
            callback();
        }
    });

    return swalAlert;
};

const displayConfirm = (alertTitle, alertMessage, confirmFunction = () => {}, otherProps = {}) => {
    let swalProps = {
        icon                : 'warning',
        title               : alertTitle,
        text                : alertMessage,
        customClass         : 'swal-confirm-box',
        allowEscapeKey      : false,
        showCancelButton    : true,
        allowOutsideClick   : false,
        cancelButtonColor   : '#d33',
        confirmButtonText   : 'Confirm',
        confirmButtonColor  : '#3085d6',
        showLoaderOnConfirm : true,
        preConfirm          : confirmFunction
    };

    if (Object.keys(otherProps).length > 0) {
        Object.assign(swalProps, otherProps);
    }

    return Swal.fire(swalProps);
};

const loadTable = (oTableElement, aData, aColumns, aColumnDefs, bSearching, initComplete) => {
    oTableElement.find('tbody').empty().parent().DataTable({
        data         : aData,
        info         : true,
        order        : [[0, 'asc']],
        columns      : aColumns,
        destroy      : true,
        ordering     : true,
        searching    : bSearching || true,
        autoWidth    : false,
        responsive   : true,
        lengthMenu   : [[4, 8, 12, 16, 20, 24, -1], [4, 8, 12, 16, 20, 24, 'All']],
        columnDefs   : aColumnDefs,
        pageLength   : 4,
        pagingType   : 'first_last_numbers',
        deferRender  : true,
        lengthChange : true,
        initComplete : initComplete || function() {}
    });
};

const inArray = (needle, haystack) => {
    return haystack.indexOf(needle) !== -1;
};

$(() => {
    // When a modal is to be closed...
    $('.modal').on('hidden.bs.modal', function () {
        // Clear all inputs inside the modal.
        clearInputs(this);
        // Reset form validations inside the modal, if any.
        const form = $(this).find('form');
        if (form.length > 0) {
            form.validate().resetForm();
        }
        // Restore vertical scroll, if multiple modals are opened.
        if ($('.modal.show').length > 0) {
            $('body').addClass('modal-open');
        }
    });
});
