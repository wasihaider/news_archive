function showNotificationError(colorName, text, placementFrom, placementAlign, animateEnter, animateExit, customVal) {
    var colorset = {
        "danger": "#d9534f",
        "warning": "#f0ad4e",
        "info": "#5bc0de",
        "success": "#5cb85c",
        "primary": "#0275d8"
    }
    if (colorName === null || colorName === '') { colorName = 'red'; }
    if (text === null || text === '') { text = 'Turning standard Bootstrap alerts'; }
    if (animateEnter === null || animateEnter === '') { animateEnter = 'animated fadeInDown'; }
    if (animateExit === null || animateExit === '') { animateExit = 'animated fadeOutUp'; }
    var allowDismiss = true;
    // colorName = 'bg-deep-orange';
    placementFrom = 'top';
    placementAlign = 'center';
    // $.notify({
    //     message: 'Momentum reduce child mortality effectiveness incubation empowerment connect.'
    // },{
    //     type: 'info',
    //     delay: 5000,
    //     icon_type: 'image',
    //     template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
    //         '<img data-notify="icon" class="img-circle pull-left">' +
    //         '<span data-notify="title">{1}</span>' +
    //         '<span data-notify="message">{2}</span>' +
    //     '</div>'
    // });
    console.log(colorName)
    $.notify({
        message:customVal 

    },
        {
            type: colorName,
            allow_dismiss: allowDismiss,
            newest_on_top: true,
            timer: 1000,
            placement: {
                from: placementFrom,
                align: placementAlign
            },
            animate: {
                enter: animateEnter,
                exit: animateExit
            },
            template: '<div data-notify="container" class="bootstrap-notify-container alert alert-dismissible {0} ' + (allowDismiss ? "p-r-35" : "") + '" role="alert" ' +
                'style="background-color: '+colorset[colorName]+'">'+
                '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                '<span data-notify="icon"></span> ' +
                '<span data-notify="title">{1}</span> ' +
                '<span data-notify="message">{2}</span>' +
                '<div class="progress" data-notify="progressbar">' +
                '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                '</div>' +
                '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>'
        });
}