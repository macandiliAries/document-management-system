const DOCS = (($) => {

    const docsTable = $('#docsTable');

    const docTypeIds = $.map($('select[name="docTypeId"] option'), (option) => option.value).filter(option => isNaN(parseInt(option, 10)) === false);

    const tableCols = [
        {
            title: 'Title', className: 'text-center doc_title', data: 'title', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Author', className: 'text-center', data: 'author', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Type', className: 'text-center', data: 'docType', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Status', className: 'text-center doc_status', data: 'status', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Approver', className: 'text-center', data: 'approver', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Effective Date', className: 'text-center', render: (data, type, row) => {
                if (row.effectiveDate === '-') {
                    return row.effectiveDate;
                }
                return moment(new Date(row.effectiveDate + '+8')).format('MMM DD, YYYY');
            }
        },
        {
            title: 'Last Updated', className: 'text-center', render: (data, type, row) => {
                if (isEmpty(row.lastEditedOn) === true) {
                    return '-';
                }
                return moment(new Date(row.lastEditedOn + '+8')).format('MMM DD, YYYY');
            }
        },
        {
            title: 'Version No.', className: 'text-center', data: 'revisionNumber', render: $.fn.dataTable.render.text()
        },
        {
            title: 'Actions', className: 'text-center', render: (data, type, row) => {
                let docsTableButtons = `
                    <button data-id="${row.docId}" class="btn btn-sm btn-primary docs-tbl-action" data-method="viewDocument"><i class="fa-solid fa-eye"></i></button>
                `;

                if (inArray(row.status, ['Draft', 'Draft Revision']) === true) {
                    docsTableButtons += `
                        <button data-id="${row.docId}" class="btn btn-sm btn-secondary docs-tbl-action" data-method="editDocument">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                        <button data-id="${row.docId}" class="btn btn-sm btn-info docs-tbl-action" data-method="submitDocumentForReview">
                            <i class="fa-solid fa-check-to-slot"></i>
                        </button>
                    `;
                }

                if (row.status === 'For Revision') {
                    docsTableButtons += `
                        <button data-id="${row.docId}" class="btn btn-sm btn-secondary docs-tbl-action" data-method="editDocument">
                            <i class="fa-solid fa-pen-to-square"></i>
                        </button>
                    `;
                }

                if (COMMON_ADMIN.currentUserType === 'Super Admin') {
                    if (inArray(row.status, ['For Review', 'For Revision Review']) === true) {
                        docsTableButtons += `
                            <button data-id="${row.docId}" class="btn btn-sm btn-success docs-tbl-action" data-method="approveDocument">
                                <i class="fa-solid fa-thumbs-up"></i>
                            </button>
                            <button data-id="${row.docId}" class="btn btn-sm btn-warning docs-tbl-action" data-method="denyDocument">
                                <i class="fa-solid fa-thumbs-down"></i>
                            </button>
                        `;
                    }

                    if (row.status === 'Approved') {
                        docsTableButtons += `
                            <button data-id="${row.docId}" class="btn btn-sm btn-warning docs-tbl-action" data-method="tagDocumentForRevision">
                                <i class="fa-solid fa-triangle-exclamation"></i>
                            </button>
                        `;
                    }

                    docsTableButtons += `
                        <button data-id="${row.docId}" class="btn btn-sm btn-danger docs-tbl-action" data-method="deleteDocument">
                            <i class="fa-solid fa-trash"></i>
                        </button>
                    `;
                }

                return docsTableButtons;
            }
        },
    ];

    const documentModal = $('#documentModal');

    const documentForm = documentModal.find('form[name="documentForm"]');

    const revisionHistoryTemplate = $('.revision-list-tpl').clone();

    const __construct = () => {
        const initialDocuments = $('input[name="documents"]');
        initializeDataTable(JSON.parse(JSON.stringify(initialDocuments.data('value'))));
        initialDocuments.remove();
        setEventHandlers();
    };

    const initializeDataTable = async (documents = []) => {
        if (documents.length === 0) {
            // Get all documents on the backend via Fetch API.
            documents = await executeRequest({
                endpoint : '/documents',
                method   : 'GET'
            });
        }

        const columnDefs = [
            { orderable  : false, targets: [2, 3, 6, -1] },
            { searchable : false, targets: [8] }
        ];

        loadTable(docsTable, documents, tableCols, columnDefs, true, function () {
            renderColumnDropdown(this, 2);
            renderColumnDropdown(this, 3);
        });
    };

    const renderColumnDropdown = (dataTable, columnNumber) => {
        const column = dataTable.api().column(columnNumber);
        const columnData = [...new Set($(column.data()))].sort(); // Get unique column data.

        let selectDropdown = $('<select></select>')
            .addClass('custom-select')
            .append(`<option value="All">${tableCols[columnNumber].title} (Show All)</option>`);

        columnData.forEach((columnValue) => {
            selectDropdown.append(`<option value="${columnValue}">${columnValue}</option>`);
        });

        selectDropdown.on('change', function () {
            const optionValue = $(this).val();
            if (optionValue === 'All') {
                return column.search('').draw();
            }
            column.search(`^${optionValue}$`, true, false).draw();
        });

        $(column.header()).html(selectDropdown);
    };

    const setEventHandlers = () => {
        $(document).on('click', 'button[data-method="viewDocument"]', async function () {
            const docId = $(this).data('id');
            const {documentDetails, revisionHistory} = await getDocumentDetails(docId);


            const viewDocumentModal = $('#viewDocumentModal');
            viewDocumentModal.find('.modal-title').text(documentDetails.title);
            viewDocumentModal.find('#documentTitle').text(documentDetails.docType);
            viewDocumentModal.find('#documentAuthor').text(documentDetails.author);
            viewDocumentModal.find('#documentContents').html(documentDetails.contents);

            toggleRevisionHistory(revisionHistory);

            viewDocumentModal.modal('show');
        });

        $(document).on('click', 'button#createDocument', () => {
            initializeWysiwyg();
            documentForm.data('operation', 'create');
            documentModal.find('.modal-title').text('Create Document');
            documentModal.modal('show');
        });

        $(document).on('click', 'button[data-method="editDocument"]', async function () {
            const docId = $(this).data('id');
            const {documentDetails} = await getDocumentDetails(docId);
            
            initializeWysiwyg(documentDetails.contents);
            documentForm.data('operation', 'edit');
            documentForm.data('document_id', docId);
            documentForm.find('input[name="title"]').prop('disabled', false).val(documentDetails.title);
            documentForm.find(`select[name="docTypeId"]`).prop('disabled', false).find(`option:contains("${documentDetails.docType}")`).prop('selected', true);

            documentModal.find('.modal-title').text('Edit Document');
            documentModal.modal('show');
        });

        $(document).on('click', 'button#submitBtn', function () {
            const formSelector = $(this).closest('form');
            initializeFormValidation(formSelector);
        });

        $(document).on('click', 'button.docs-tbl-action:not([data-method="editDocument"], [data-method="viewDocument"])', function () {
            const docTitle = $(this).closest('tr').find('td.doc_title').text();
            const docStatus = $(this).closest('tr').find('td.doc_status').text();

            const action = $(this).data('method');
            const actions = {
                submitDocumentForReview : {
                    confirmTitle   : `Submit ${docStatus} Document`,
                    confirmMessage : (docStatus === 'Draft') ? `Are you sure you want to submit the ${docTitle} document for review?` : 'Please enter the significant changes made to the document.'
                },
                approveDocument         : {
                    confirmTitle   : 'Approve Document',
                    confirmMessage : `Are you sure you want to grant approval for the ${docTitle} document?`
                },
                denyDocument            : {
                    confirmTitle   : 'Deny Document',
                    confirmMessage : `Are you sure you want to deny approval for the ${docTitle} document?`
                },
                tagDocumentForRevision  : {
                    confirmTitle   : 'Tag Document for Revision',
                    confirmMessage : `Are you sure you want to tag the ${docTitle} document for revision?`
                },
                deleteDocument          : {
                    confirmTitle   : 'Delete Document',
                    confirmMessage : `Are you sure you want to permanently delete the ${docTitle} document?`
                }
            }

            if (inArray(action, Object.keys(actions)) === false) {
                return displayAlert(false, 'Invalid Request', 'Invalid document operation.');
            }

            let otherSwalProps = {};
            const toSubmitDraftRevisionForReview = (action === 'submitDocumentForReview' && docStatus === 'Draft Revision');
            if (toSubmitDraftRevisionForReview === true) {
                $.extend(otherSwalProps, {
                    input          : 'textarea',
                    inputValidator : (significantChanges) => {
                        if (isEmpty(significantChanges.trim()) === true) {
                            return 'Revision details should not be left blank.'
                        }
                    }
                });
            }

            displayConfirm(actions[action]['confirmTitle'], actions[action]['confirmMessage'], async (significantChanges = '') => {
                let fetchProps = {
                    endpoint : `/documents/${$(this).data('id')}`,
                    method   : 'PATCH',
                    body     : {
                        operation : action
                    }
                };

                if (toSubmitDraftRevisionForReview === true) {
                    $.extend(fetchProps['body'], { significantChanges });
                }

                return await executeRequest(fetchProps);
            }, otherSwalProps).then((result) => {
                if (result.isConfirmed === false) {
                    return false;
                }

                const response = result.value;
                displayAlert(response.result, response.title, response.message, () => {
                    if (response.result === true) {
                        initializeDataTable();
                    }
                });
            });
        });
    };

    const initializeFormValidation = (formSelector) => {
        let formValidationRules = {
            submitHandler  : () => {
                if (checkSummernoteContents() === true) {
                    const alertTitle   = `${((formSelector.data('operation') === 'create') ? 'Create' : 'Update')} Document`;
                    const alertMessage = `Are your sure you want to ${((formSelector.data('operation') === 'create') ? 'create a new' : 'update this existing')} document?`;
                    displayConfirm(alertTitle, alertMessage, () => submitDocument(formSelector));
                }
             },
            errorElement   : 'small',
            errorPlacement : (errorLabel, elementToValidate) => {
                errorLabel.addClass('mt-n2 mb-n2 form-text text-danger text-right');
                elementToValidate.closest('div.form-group').append(errorLabel);
            },
            rules: {
                title     : {
                    required  : true,
                    minlength : 3
                },
                docTypeId : {
                    required      : true,
                    allowedValues : docTypeIds
                }
            },
            messages: {
                title     : {
                    required  : 'Please enter a title for the document.',
                    minlength : 'Please enter at least 3 characters for the document title.',
                },
                docTypeId : {
                    required      : 'Please select a document type.',
                    allowedValues : 'Please select a valid document type.'
                }
            }
        };

        checkSummernoteContents();
        $(document).on('input', '.note-editable.card-block', checkSummernoteContents);
        formSelector.validate(formValidationRules);
        formSelector.trigger('submit');
    };

    const checkSummernoteContents = () => {
        const contentsSelector = $('#contents');
        contentsSelector.closest('div.form-group').find('small#summernoteErrorLabel').remove();
        if (contentsSelector.summernote('isEmpty') === true) {
            contentsSelector.closest('div.form-group').append(`
                <small class="pt-2 mb-n3 form-text text-danger text-right" id="summernoteErrorLabel">
                    Please enter some content for the document.
                </small>
            `);
            return false;
        }
        return true;
    }

    const submitDocument = async (formSelector) => {
        let requestData = getRequestData(formSelector);

        const operation = formSelector.data('operation');
        $.extend(requestData, {
            contents : $('#contents').summernote('code'),
        });

        if (operation !== 'create') {
            $.extend(requestData, {
                operation : operation
            });
        }

        toggleInputs('disable');
        toggleSpinner('show');

        const response = await executeRequest({
            endpoint : (operation === 'create') ? '/documents' : `/documents/${formSelector.data('document_id')}`,
            method   : (operation === 'create') ? 'POST' : 'PATCH',
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

    const toggleRevisionHistory = (revisionHistory) => {
        const revisionHistoryDiv = $('.revision-history-div');
        if (revisionHistory.length <= 1) {
            revisionHistoryDiv.hide();
            return;
        }

        revisionHistoryDiv.show();
        const revisionListArea = $('.revision-list-area');
        revisionListArea.find('div[class!="revision-list-tpl"]').remove();

        for (data of revisionHistory) {
            let oRow = revisionHistoryTemplate.clone().attr({
                'hidden' : false,
                'class'  : 'revision-list-tpl-clone'
            });

            oRow.find('#dateRevised').text(moment(new Date(data.dateRevised + '+8')).format('MMM DD, YYYY @ hh:mm A'));
            oRow.find('#revisionNumber').text(data.revisionNumber);
            oRow.find('#revisedBy').text(data.revisedBy);
            oRow.find('#significantChanges').text(data.significantChanges);

            if (data.revisionNumber === 'v1.0') {
                oRow.find('#revisedBy').prev('label').text('Created by')
            }

            revisionListArea.append(oRow);
        }
    }

    const initializeWysiwyg = (contents) => {
        const wysiwyg = $('#contents');
        wysiwyg.summernote({
            height               : 400,
            tabsize              : 2,
            toolbar              : [
                ['style', ['style']],
                ['fontname', ['fontname']],
                ['fontsize', ['fontsize']],
                ['color', ['color']],
                ['font', ['bold', 'underline', 'clear', 'strikethrough', 'superscript', 'subscript']],
                ['para', ['ul', 'ol', 'paragraph', 'hr']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'help']],
            ],
            tabDisable           : true,
            placeholder          : 'Type here.',
            dialogsFade          : true,
            dialogsInBody        : true,
            codeviewFilter       : true,
            codeviewIframeFilter : true
        });

        if (isEmpty(contents) === false) {
            wysiwyg.summernote('code', contents);
        }
    };

    const getDocumentDetails = async (docId) => {
        return await executeRequest({
            endpoint : `/documents/${docId}`,
            method   : 'GET'
        });
    };

    return {
        initialize : __construct
    };

})(jQuery);

$(() => {
   DOCS.initialize(); 
});