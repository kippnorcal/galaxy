$(function () {
    $('[data-toggle="tooltip"]').tooltip();

    $('[data-toggle="tooltip"]').click(function () {
        $('[data-toggle="tooltip"]').tooltip('hide');
    });
})