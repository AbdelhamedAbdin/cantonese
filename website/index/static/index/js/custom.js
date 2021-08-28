$(document).ready(function() {
    // Add active on category
    let access_url = window.location,
        target_url = $("nav .taping a").toArray(),
        i;
    for (i = 0; i < target_url.length; i++) {
        let target = target_url[i];
        if (access_url.pathname == target.pathname) {
            $(target).addClass("active").siblings().removeClass("active");
        } else {
            $(target).removeClass("active");
        }
    }

    // Add classes on login form
    $('.login input[type="text"]').attr({"placeholder": "Email", 'class': 'form-control'});
    $('.login input[type="password"]').attr({"placeholder": "Password", 'class': 'form-control', 'id': 'password-field'});

    // add style on search history
    let search_history = $("#search-history");

    // Popover event
    $(function () {
        $('.fa-trash').popover({
            container: 'body',
            trigger: 'hover'
        })
    });

    $(function () {
        $('.fa-star').popover({
            container: 'body',
            trigger: 'hover'
        })
    });

    // call Redo form
    let history_id = $('.history_id');
    history_id.on('click', function () {
       $($(this).data('historyid')).click();
    })

    // The frame of the data table of history page on profile
    $(document).ready( function () {
        $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
            let table = $('#table_id').DataTable({
                responsive: true,
                bPaginate: false,
                paging: false,
                ordering: false,
                info: false
            }).columns.adjust().responsive.recalc();
        })
    });
});