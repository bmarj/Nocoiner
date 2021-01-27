$(document).ready(
    function () {
        setupAll(); 
    }
);

function setupAll() {
    disableSubmitOnEnter();
    setupInlineAdd();
    setupTable();
    //setupColvisButton();
    //setupDatatable();
    //setupDatePicker();
    setupFileUpload();
    disableFormAutocomplete();    
}

function setupTable() {
    // double click behavior
    // $("table.table-hover tbody tr").dblclick(function () {
    //     var links = this.getElementsByTagName("a");
    //     if (links.length > 0)
    //         window.location = links[0].href;
    // }
    // );

    // select/deselect row on click
    // turned on for tables with .clickable-rows class
    $("table.clickable-rows tbody tr").on("click", function (event) {
        rowClass = 'selected';
        if ($(this).hasClass(rowClass)) {
            $(this).removeClass(rowClass);
        } else {
            $(this).addClass(rowClass).siblings().removeClass(rowClass);
        }
    });

    // fix za datatables unutar bootstrap tabova
    // nije radilo na grupiranom gridu,
    // umjesto ovoga postavio style = "width: 100% !important" na gridu 
    //
    //$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
    //    $.fn.dataTable.tables({ visible: true, api: true })
    //        .columns.adjust()
    //        .responsive.recalc()
    //        .draw();
    //})
}

function setupColvisButton(){
    $("button.buttons-colvis")
        .removeClass('dt-button buttons-collection buttons-colvis')
        .addClass('btn btn-outline-secondary btn-sm');

};

// setup image preview
function handleFiles(files, previewDivId) {
    for (let i = 0; i < files.length; i++) {
        const file = files[i];

        if (!file.type.startsWith('image/')) { continue }

        const img = document.createElement("img");
        img.classList.add("obj");
        img.width = 500;
        img.file = file;

        var preview = document.querySelector('#' + previewDivId);
        preview.innerHTML = null;
        preview.appendChild(img); // Assuming that "preview" is the div output where the content will be displayed.

        const reader = new FileReader();
        reader.onload = (function (aImg) { return function (e) { aImg.src = e.target.result; }; })(img);
        reader.readAsDataURL(file);
    }
}

// set filename view
function handleSelectFile(input) {
    //var fileName = $(input).val().split('\\').pop();
    //$(input).next('').html(fileName);
    setUploadFiles(input, input.files, true);
}

function setupFileUpload() {
    let inp = $("input[type=file]");
    inp.each(setupDragAndDropFiles);
}

// set drag and drop functionality for multiupload control
// binds to closest element with class="drop-area"
function setupDragAndDropFiles(index, fileInput) {
    let dropArea = $(fileInput).closest('.drop-area')[0];
    if (!dropArea)
        return;

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false)
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false)
    });

    function highlight(e) {
        dropArea.classList.add('highlight')
    }

    function unhighlight(e) {
        dropArea.classList.remove('highlight')
    }

    // dragover and dragenter events need to have 'preventDefault' called
    // in order for the 'drop' event to register. 
    // See: https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Drag_operations#droptargets
    dropArea.ondragover = dropArea.ondragenter = function (evt) {
        evt.preventDefault();
    };

    dropArea.ondrop = function (evt) {
        evt.preventDefault();
        getFilesRecursively(fileInput, evt.dataTransfer);
    };
}

// set file list for custom file upload 
function setUploadFiles(fileInput, files, removeOtherFiles = false) {
    let filesListingDiv = $("#" + fileInput.getAttribute("file-list-id") + " .added");

    // pretty simple -- but not for IE :(    
    let fileNameArray = [...files].map(e => e.name);
    if (removeOtherFiles) {
        fileInput.files = files;
        filesListingDiv.html(fileNameArray.join("<br/>") + "<br/>");
    } else {
        const dataTransfer = new DataTransfer();
        for (var i = 0; i < fileInput.files.length; i++) {
            dataTransfer.items.add(fileInput.files[i])
        }
        for (var i = 0; i < files.length; i++) {
            dataTransfer.items.add(files[i])
        }        
        fileInput.files = dataTransfer.files;
        filesListingDiv.html(filesListingDiv.html() + fileNameArray.join("<br/>") + "<br/>");
    }        
}

// recursively add files in folders, 
// it is async so I pass in input control and update it
function getFilesRecursively(fileInput, dataTransfer) {
    var items = dataTransfer.items;
    for (var i = 0; i < items.length; i++) {
        // webkitGetAsEntry is where the magic happens
        var item = items[i].webkitGetAsEntry();
        if (item) {
            traverseFileTree(item, "", fileInput);
        }
    }
}

function traverseFileTree(item, path, fileInput) {
    path = path || "";
    if (item.isFile) {
        // Get file
        item.file(function (file) {
            setUploadFiles(fileInput, [file], false)
        });
    } else if (item.isDirectory) {
        // Get folder contents
        var dirReader = item.createReader();
        dirReader.readEntries(function (entries) {
            for (var i = 0; i < entries.length; i++) {
                traverseFileTree(entries[i], path + item.name + "/", fileInput);
            }
        });
    }
}

// setup image preview
function setFilename(input, targetId) {
    var fileName = $(input).val().split('\\').pop();
    document.getElementById(targetId).value = fileName;
    //$(targetId).text(fileName);
}

function formatResult(item) {
    // because of the placeholder
    if (!item.id)
        return item.text;

    //element = '<span class="control-text" ';
    //if (item.element.attributes['data-level'])
    //    element = element + 'style="padding-left: ' + parseInt(item.element.attributes['data-level'].value) * 20 + 'px"';
    //element = element + '>' + item.text;
    //element = element + '</span>';

    //var $element = $(item.element);

    var $wrapper = $('<span class="control-text"></span>');
    $wrapper.addClass(item.element.className);

    $wrapper.text(item.text);

    return $wrapper;
}

function formatSelected(item) {
    // because of the placeholder
    if (!item.id)
        return item.text;

    opt = $(item.element);

    sel = opt.text();
    og = opt.closest('optgroup').attr('label');
    element = '<span class="control-text">' +
        item.text;
    if (og != undefined)
        element = element + ' - <b>' + og + '</b>';
    element = element + '</span>';

    return element;
}

function setupSelect() {
    var s = $('select.select2');
    s.select2(
        {
            hidePlaceholder: true,
            placeholder: '-- select -- ',
            //multiple: true,
            //maximumSelectionLength: 2,
            allowClear: true,
            templateSelection: formatSelected,
            escapeMarkup: function (m) { return m; },
            templateResult: formatResult,
        }
    );

    var s = $('select.select2-to-tree');
    s.select2ToTree(
        {
            hidePlaceholder: true,
            placeholder: '-- select -- ',
            //multiple: true,
            //maximumSelectionLength: 2,
            allowClear: true,
            templateSelection: formatSelected,
            escapeMarkup: function (m) { return m; },
            templateResult: formatResult,
        }
    );
}


// Class definition
var controls = {
    leftArrow: '<i class="fal fa-angle-left" style="font-size: 1.25rem"></i>',
    rightArrow: '<i class="fal fa-angle-right" style="font-size: 1.25rem"></i>'
}

function setupDatePicker() {
    // minimum setup
    $(".datepicker").datepicker(
        {
            todayHighlight: false,
            orientation: "bottom left",
            templates: controls,
            autoclose: true,
            format: 'yyyy-mm-dd',
            forceParse: true,
            language: 'hr',
            weekStart: 1
        });
}


function setupDatatable() {
    var tbs = $('.table-datatable');
    tbs.toArray().forEach(function (tb) {
        // var group = tb.querySelectorAll('th[group]');
        var headers = tb.querySelectorAll('th');
        groupList = []
        for (var i = 0; i < headers.length; i++) {
            if (headers[i].getAttribute('group') != null)
                groupList.push(i);
        }

        var rowGroupSettings = null;
        var columnDefsSettings = null;
        if (groupList.length > 0) {
            rowGroupSettings = {
                dataSrc: groupList
            }
            columnDefsSettings = [{
                targets: groupList,
                visible: false
            }]
        }

        let lengthMenuItems = [
            [10, 20, 50, 200, -1],
            [10, 20, 50, 200, "Sve"]
        ];

        $(tb).DataTable(
            {
                responsive: false,
                fixedHeader: true,
                paging: true,
                lengthMenu: lengthMenuItems,
                pageLength: -1,
                processing: false,
                //columnDefs: [
                //    { "type": "num", "targets": 0 }
                //]
                rowGroup: rowGroupSettings,
                columnDefs: columnDefsSettings
            })
    });


    $('.js-thead-colors a').on('click', function () {
        var theadColor = $(this).attr("data-bg");
        console.log(theadColor);
        $('#grid thead').removeClassPrefix('bg-').addClass(theadColor);
    });

    $('.js-tbody-colors a').on('click', function () {
        var theadColor = $(this).attr("data-bg");
        console.log(theadColor);
        $('.table-datatable').removeClassPrefix('bg-').addClass(theadColor);
    });

};

// find table related to button element
function findRelatedTable(sender) {
    // strategy 1: explicit table ID on button element
    var gridID = sender.getAttribute('data-grid');
    if (gridID) {
        var table = $('#' + gridID);
        if (table.length != 0)
            return table;
        // if explicitly defined id is definite
        else return null;
    }

    // strategy 2: explicit table ID on parent element
    gridID = sender.parentElement.getAttribute('data-grid');
    if (gridID) {
        var table = $('#' + gridID);
        if (table.length != 0)
            return table;
        // if explicitly defined id is definite
        else return null;
    }

    // // strategy 3: inside table >thead>tr>th>div
    // var table = $(sender).closest('table');
    // if (table.length != 0)
    //     return table;

    // // strategy 4: inside div before table
    // table = $(sender).parent().nextAll('table').first();
    // if (table.length != 0)
    //     return table;

    // // strategy 5: inside div before datatable wrapper
    // table = $(sender).parent().nextAll('.dataTables_wrapper').find('table').first();
    // if (table.length != 0)
    //     return table;

    // strategy 6: inside card-body
    table = $(sender).closest('.card').find('table').first();
    if (table.length != 0)
        return table;
}

// get rows selected on a table
function getSelectedRows(table) {
    return table.find('.selected');
}

// get array of attribute values
function getRowAttributes(tableRows, attributeName) {
    // short way: 
    // var ids = tableRows.toArray().map(el => el.attributes["id"].value);
    var ids = tableRows.toArray()
        .map(
            function (row) {
                return row.attributes[attributeName].value
            }
        );
    return ids;
}

// get array of id values
function getRowIds(tableRows) {
    return getRowAttributes(tableRows, "id");
}

// open edit page
function goToEdit(sender, urlToAction) {
    let url = getEditUrl(sender, urlToAction);
    if (url){
        window.location.href = url;
    }        
}

function getEditUrl(sender, urlToAction) {
    var table = findRelatedTable(sender);
    var selectedRows = getSelectedRows(table);
    if (selectedRows.length == 0) {
        alert("Click on the row to select it.");
    }
    else if (selectedRows.length > 1) {
        alert("Select single row.");
    }
    else if (selectedRows.length == 1) {
        var urlReplaced = urlToAction;
        // support for multiple placeholders
        // replace on by one
        while (hasExpression = urlReplaced.match(/\{(.*?)\}/)) {
            var attrName = hasExpression[1];
            var attrValues = getRowAttributes(selectedRows, attrName);
            urlReplaced = urlReplaced.replace('{' + attrName + '}', attrValues[0]);
        }

        // if url string is changed with placeholders, use it
        if (urlReplaced != urlToAction) 
            url = urlReplaced;
        else {
            // ordinary edit by id
            var ids = getRowIds(selectedRows);
            url = urlToAction 
                + (urlToAction[urlToAction.length-1] =='/' ? '' : '/') // appends slash if not url doesn't end with one
                + ids[0];
        }
        return url;
    }
    return false;
}

// go to delete action
function doActionPost(sender, urlToAction, dialogId) {
    var table = findRelatedTable(sender);
    var selectedRows = getSelectedRows(table);
    if (selectedRows.length == 0) {
        alert("Click on the row to select it.");
    }
    else if (selectedRows.length > 1) {
        alert("Select single row.");
    }
    else if (selectedRows.length == 1) {
        if (confirmAction(sender)) {

            if (urlToAction == null)
                return true;
            var hasExpression = urlToAction.match(/\{(.*?)\}/);
            if (hasExpression) {
                // custom edit by expresssion
                var attrName = hasExpression[1];
                var attrValues = getRowAttributes(selectedRows, attrName);

                var url = urlToAction.replace('{' + attrName + '}', attrValues[0]);
                // go to url
                // window.location.href = url;                
                $.ajax({
                    type: 'POST',
                    //dataType: "json",
                    url: url,
                    encode: true,
                    success: function(data) {
                        $(dialogId).replaceWith(data);
                    },
                    error: function(e) { 
                        alert('Error. Try again.');
                    }
                });
            }
            else {
                // ordinary edit by id
                var ids = getRowIds(selectedRows);
                var url = urlToAction + '/' + ids[0];
                // go to url
                //window.location.href = url;
                $.ajax({
                    type: 'POST',
                    //dataType: "json",
                    url: url,
                    encode: true,
                    success: function(data) {
                        $(dialogId).replaceWith(data);
                    },
                    error: function(e) { 
                        alert('Error. Try again.');
                    }
                });
            }
        }
    }
    return false;
}


// open edit modal
function goToEditModal(sender, urlToAction, dialogId) {
    let url = getEditUrl(sender, urlToAction);
    if (url){
        $.ajax({
            //dataType: "json",
            url: url,
            //data: data,
            success: function(data) {
                // IS REDIRECT TO LOGIN?  
                if (data.trimStart().startsWith("<!DOCTYPE html>")){
                    window.location = window.location.origin + '/login?returnUrl=' + url;
                    //$(document).replaceWith(data);
                }
                else{
                    // $('#editModal').modal('hide');
                    $(dialogId).replaceWith(data);
                }
            },
            error: function(e) { alert('Error. Try again.');}
        });
    }        
}

// function formValidate(form){
//     if (form.hasClass('validate') && form[0].checkValidity === false) {
//         // e.preventDefault();
//         // e.stopPropagation();
//         form.addClass('was-validated');
//         return false;
//     }
//     form.addClass('was-validated');
//     return true;
// }


function submitModal(sender, urlToAction, dialogId) {
    let url = urlToAction;
    if (url){
        var form = $(dialogId + " form");

        var formData = form.serialize();
        $.ajax({
            type: 'POST',
            //dataType: "json",
            url: url,
            data: formData,
            encode: true,
            success: function(data) {
                // IS REDIRECT TO LOGIN?  
                if (data.trimStart().startsWith("<!DOCTYPE html>")){
                    window.location = window.location.origin + '/login?returnUrl=' + url;
                    //$(document).replaceWith(data);
                }
                else{
                    $('#editModal').modal('hide');
                    $(dialogId).replaceWith(data);
                }
            },
            error: function(e) { 
                alert('Error. Try again.');
            }
        });
    }        
}

function closeModal(dialogId) {
    $(dialogId).modal('hide');
}

function setupModal(){
    $('button[data-dismiss]').on('click', function(){ closeModal('#editModal'); });
    // fields without name are not posted, so make them readonly
    $("form input:not([name])").attr('disabled', '');
    handleValidation();
    //setupSelect();

    $('#editModal').on('shown.bs.modal', makeModalDraggable);

}

function makeModalDraggable(event){
    // setup jQueryUI draggable modal dialog
    // only if jQueryUI exists
    if ($().resizable != undefined)
    {
        $('.modal-content').resizable({
            //alsoResize: ".modal-dialog",
            minHeight: $('.modal-content').height(),
            minWidth: 300
          });
        $('.modal-dialog').draggable();
      
        $('#editModal').on('show.bs.modal', function() {
            $(this).find('.modal-body').css({
                'max-height': '100%'
            });
        });
    }
}

// go to delete action
function doDelete(sender, urlToAction, checkOnly) {
    var table = findRelatedTable(sender);
    var selectedRows = getSelectedRows(table);
    if (selectedRows.length == 0) {
        alert("Click on the row to select it.");
    }
    else if (selectedRows.length > 1) {
        alert("Select single row.");
    }
    else if (selectedRows.length == 1) {
        if (confirmDelete(sender)) {

            if (checkOnly || urlToAction == null)
                return true;
            var hasExpression = urlToAction.match(/\{(.*?)\}/);
            if (hasExpression) {
                // custom edit by expresssion
                var attrName = hasExpression[1];
                var attrValues = getRowAttributes(selectedRows, attrName);

                var url = urlToAction.replace('{' + attrName + '}', attrValues[0]);
                // go to url
                window.location.href = url;
            }
            else {
                // ordinary edit by id
                var ids = getRowIds(selectedRows);
                var url = urlToAction + '/' + ids[0];
                // go to url
                window.location.href = url;
            }
        }
    }
    return false;
}

function confirmDelete(sender) {
    if (confirm('Are you sure you want to delete this data?')) {
        return true;
    }
    return false;
}

function confirmAction(sender) {
    let message = $(sender).data('confirmation-message');
    // if data-confirmation-message is not defined on button, skip confirmation
    if (message === undefined)
        return true;
    if (confirm(message)) {
        return true;
    }
    return false;
}

// set href for ajax call
function setHrefAttr(sender) {
    var table = findRelatedTable(sender);
    var selectedRows = getSelectedRows(table);
    if (selectedRows.length == 1) {
        var urlToAction = sender.attributes['href'].value;
        var hasExpression = urlToAction.match(/\{(.*?)\}/);
        if (hasExpression) {
            // custom edit by expresssion
            var attrName = hasExpression[1];
            var attrValues = getRowAttributes(selectedRows, attrName);
            var url = urlToAction.replace('{' + attrName + '}', attrValues[0]);
            sender.setAttribute('data-ajax-url', url);
        }
        else {
            // ordinary edit by id
            var ids = getRowIds(selectedRows);
            var url = urlToAction + '/' + ids[0];
            sender.setAttribute('data-ajax-url', url);
        }
    }
}

function toggleExpandIcon(button) {
    var target = button.attributes["data-target"].value;
    button.disabled = true;
    if (button.innerHTML.includes("fal fa-plus")) {
        $(target).collapse("show").on('shown.bs.collapse', function (btn) {
            btn.innerHTML = "<i class=\"fal fa-minus\"></i>";
            btn.disabled = false;
        }(button));
        //button.innerHTML = "<i class=\"fal fa-minus\"></i>";
    }
    else {
        $(target).collapse("hide").on('hidden.bs.collapse', function (btn) {
            btn.innerHTML = "<i class=\"fal fa-plus\"></i>";
            btn.disabled = false;
        }(button));
        //button.innerHTML = "<i class=\"fal fa-plus\"></i>";
    }
}


// inline add:
function applyInlineAddState(btn) {
    if (btn.getAttribute('data-adding') == "true") {
        btn.innerHTML = '<i class="fal fa-eject mr-1"></i>Cancel';
        $('#' + btn.getAttribute('data-edit-form')).show(300);
    }
    else {
        btn.innerHTML = '<i class="fal fa-plus mr-1"></i>Add';
        $('#' + btn.getAttribute('data-edit-form')).hide(300);
    }
}
function toggleInlineAdd(btn) {
    btn.setAttribute('data-adding', btn.getAttribute('data-adding') == "false" ? "true" : "false");
    applyInlineAddState(btn);
}

function setupInlineAdd() {
    var els = document.querySelectorAll("[data-adding]:not([initialized])");
    els.forEach(function (btn) {
        btn.addEventListener("click", function () {
            toggleInlineAdd(btn);
        });
        applyInlineAddState(btn);
        // prevent multiple initializations from adding multiple event handlers
        btn.setAttribute("initialized", "");
    });
}

function getSelect2SelectedTextByID(fieldId) {
    if ($('select#' + fieldId + '.select2').length > 0)
        return $('select#' + fieldId).select2("data")[0].text;
    return "";
}

function getCheckboxChecked(fieldId, ignoreMissing = true) {
    let idSelector = '#' + fieldId;
    if ($(idSelector).length != 1 && ignoreMissing)
        throw 'Control with id ' + fieldId + ' not found!'
    if ($(idSelector + ':checked').length != 0)
        return true;
    else
        return false;
}

//function closePage(sender, e) {
//    ////var numberOfEntries = window.history.length;
//    //window.history.go(-1);
//    //e.preventDefault();
//    return True;
//}


// prevents Submit on Enter key
function disableSubmitOnEnter() {
    $(document).keypress(function (e) {
        if (e.keyCode === 13) {
            e.preventDefault();
            return false;
        }
    });
}

//Disable autocomplete throughout the site
function disableFormAutocomplete() {
    $("input:text,form").attr("autocomplete", "off");
}

var handleValidation = function () {
    $('.validate').on('submit', function (e) {
        e.preventDefault();

        var form = $('.validate');

        if (form[0].checkValidity === false) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.addClass('was-validated');
    });
}

var defaultDatatablesDOM = 
    //"<'row'<'col-sm-12 offset-11 col-md-1'B>>" +
    "<'row'<'col-sm-12 col-md-4'l><'col-sm-12 col-md-4'B><'col-sm-12 col-md-4'f>>" +
    "<'row'<'col-sm-12'tr>>" +
    "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>";
let lengthMenuItems = [
    [10, 15, 20, 50, 100],
    ['10', '15', '20', '50', '100']
];
var defaultDatatablesConfig =
{
    processing: false, // for "Processing" message
    serverSide: true,    
    filter: true,
    deferRender: true,    
    rowId: 'id',
    dom: defaultDatatablesDOM,
    colReorder: true,
    stateSave: true,
    buttons: [
        {
            extend: 'colvis',
            class: 'btn btn-outline-secondary'
            //collectionLayout: 'fixed two-column'
        }
    ],
    ajax: {
        error: function(xhr, error, thrown) {
            if (xhr.status == 401) {
                window.location = window.location.origin + '/login?returnUrl=' + window.location.pathname;
                return false;
            }          
        }
    },
    lengthMenu: lengthMenuItems,
    pageLength: 10
}

function initDatatable(datatableId, dtConf){    
    // default empty string content for values returned as null
    dtConf.columns.forEach((t) => t.defaultContent === undefined ? t.defaultContent = "" : null);
    let table = $(datatableId);
    table
        .on('draw.dt', function(e, settings, data, xhr) {
            setupTable();
        } )
        .DataTable(dtConf);
    setupColvisButton();
}
