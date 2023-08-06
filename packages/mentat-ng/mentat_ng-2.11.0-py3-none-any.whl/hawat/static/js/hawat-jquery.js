/*******************************************************************************

    jQuery and Bootstrap related functions.

*******************************************************************************/

$(function() {

    const createTempusDominusInstance = (elementId, options) => {
        const element = document.getElementById(elementId);
        return new tempusDominus.TempusDominus(element, options);
    };
    const createCommonOptions = (_format, _useSeconds) => {
        return {
            localization: {
                locale: GLOBAL_LOCALE,
                format: _format,
                startOfTheWeek: 1,
                hourCycle: 'h23'
            },
            display: {
                icons: {
                    time: "fas fa-fw fa-clock",
                    date: "fas fa-fw fa-calendar-alt",
                    up: "fas fa-fw fa-arrow-up",
                    down: "fas fa-fw fa-arrow-down",
                    previous: 'fas fa-chevron-left',
                    next: 'fas fa-chevron-right'
                },
                components: {
                    seconds: _useSeconds
                },
                theme: 'light'
            }
        }
    };

    // Initialize date and datetime picker components.
    const commonOptionsSeconds = createCommonOptions('yyyy-MM-dd HH:mm:ss', true);
    if (document.getElementById('datetimepicker-from') && document.getElementById('datetimepicker-to')) {
        const linked_from_1 = createTempusDominusInstance('datetimepicker-from', commonOptionsSeconds);
        const linked_to_1 = createTempusDominusInstance('datetimepicker-to', {
            useCurrent: false,
            ...commonOptionsSeconds
        });
        document.getElementById('datetimepicker-from').addEventListener(tempusDominus.Namespace.events.change, (e) => {
            linked_to_1.updateOptions({
                restrictions: {
                    minDate: e.detail.date,
                },
            });
        });
        document.getElementById('datetimepicker-to').addEventListener(tempusDominus.Namespace.events.change, (e) => {
            linked_from_1.updateOptions({
                restrictions: {
                    maxDate: e.detail.date,
                },
            });
        });
    }
    if (document.getElementById('datetimepicker-from-2') && document.getElementById('datetimepicker-to-2')) {
        const linked_from_2 = createTempusDominusInstance('datetimepicker-from-2', commonOptionsSeconds);
        const linked_to_2 = createTempusDominusInstance('datetimepicker-to-2', {
            useCurrent: false,
            ...commonOptionsSeconds
        });
        document.getElementById('datetimepicker-from-2').addEventListener(tempusDominus.Namespace.events.change, (e) => {
            linked_to_2.updateOptions({
                restrictions: {
                    minDate: e.detail.date,
                },
            });
        });
        document.getElementById('datetimepicker-to-2').addEventListener(tempusDominus.Namespace.events.change, (e) => {
            linked_from_2.updateOptions({
                restrictions: {
                    maxDate: e.detail.date,
                },
            });
        });
    }
    const commonOptions = createCommonOptions('yyyy-MM-dd HH:mm', false);
    if (document.getElementById('datetimepicker-hm-from') && document.getElementById('datetimepicker-hm-to')) {
        const linked_from = createTempusDominusInstance('datetimepicker-hm-from', commonOptions);
        const linked_to = createTempusDominusInstance('datetimepicker-hm-to', {
            useCurrent: false,
            ...commonOptions
        });
        document.getElementById('datetimepicker-hm-from').addEventListener(tempusDominus.Namespace.events.change, (e) => {
            linked_to.updateOptions({
                restrictions: {
                    minDate: e.detail.date,
                },
            });
        });
        document.getElementById('datetimepicker-hm-to').addEventListener(tempusDominus.Namespace.events.change, (e) => {
            linked_from.updateOptions({
                restrictions: {
                    maxDate: e.detail.date,
                },
            });
        });
    }

    // Initialize select pickers.
    //$('.selectpicker').selectpicker();

    // Initialize tooltips.
    $('body').tooltip({
        selector: "[data-toggle=tooltip]",
        container: "body",
    });

    // Tooltips for navbar tabs require special handling.
    $('.nav-tabs-tooltipped').tooltip({
        selector: "[data-toggle=tab]",
        trigger: 'hover',
        placement: 'top',
        animate: true,
        container: 'body'
    });

    // Initialize popovers.
    $('body').popover({
        selector: "[data-toggle=popover]",
    });
    // Custom popovers implemented using @popperjs/core library. The Bootstrap variant
    // does not support some advanced features.
    $('.popover-hover-container').on("mouseenter", ".popover-hover", function() {
        var ref = $(this);
        var popup = $($(this).attr("data-popover-content"));
        popup.toggleClass("hidden static-popover");
        var popper = Popper.createPopper(ref[0], popup[0], {
            placement: 'top',
            onCreate: function(data) {
                popup.find('.popover').removeClass('top');
                popup.find('.popover').removeClass('bottom');
                popup.find('.popover').addClass(data.placement);
                popper.update();
            },
            onUpdate: function(data) {
                popup.find('.popover').removeClass('top');
                popup.find('.popover').removeClass('bottom');
                popup.find('.popover').addClass(data.placement);
                popper.update();
            },
            modifiers: {
                flip: {
                    behavior: ['top','bottom']
                }
            }
        });
        ref.data('popper-instance', popper);
    });
    $('.popover-hover-container').on("mouseleave", ".popover-hover", function() {
        var ref = $(this);
        var popup = $($(this).attr("data-popover-content"));
        popup.toggleClass("hidden static-popover");
        var popper = ref.data('popper-instance');
        if (popper) {
            popper.destroy();
            ref.data('popper-instance', null);
        }
    });

    // Callback for triggering re-render of NVD3 charts within the bootstrap tabs.
    // Without this function the charts on invisible tabs are rendered incorrectly.
    // References:
    //      https://stackoverflow.com/questions/32211346/chart-update-when-bootstrap-tab-changed
    //      https://stackoverflow.com/a/47521742
    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        // Each tab navigation link points to the tab panel. Use this link
        // to get IDs of all subsequent chart containers. These IDs match the
        // IDs of the charts, use this information to update correct chart.
        $(e.currentTarget.hash + ' div.chart-container').each(function(idx) {
            console.log("Updating visualisation: " + this.id);
            update_visualisation(this.id);
        });
        // Original and now deprecated solution was really slow, because it
        // triggered update on all charts on the page, regardless of their
        // visibility to the user.
        //window.dispatchEvent(new Event('resize'));
    });

    // Callback for triggering re-render of NVD3 charts after the collapse transition
    // (collapsible sidebar for timeline charts).
    // Resources:
    //      https://stackoverflow.com/questions/9255279/callback-when-css3-transition-finishes
    //      https://stackoverflow.com/a/47521742
    $(".column-chart-sidebar").bind("transitionend webkitTransitionEnd oTransitionEnd MSTransitionEnd", function(e) {
        // Sibling of each sidebar is the container for chart. Its ID matches the
        // ID of the chart, so it is possible to trigger the update.
        $('#' + e.currentTarget.previousElementSibling.id + ' div.chart-container').each(function(idx) {
            console.log("Updating visualisation: " + this.id);
            update_visualisation(this.id);
        });
        // Original and now deprecated solution was really slow, because it
        // triggered update on all charts on the page, regardless of their
        // visibility to the user.
        //window.dispatchEvent(new Event('resize'));
    });

    // Special handling of '__EMPTY__' and '__ANY__' options in event search form
    // selects. This method stil can be improved, so that 'any' is capable of disabling
    // 'empty'.
    //$(".esf-any-empty").on("changed.bs.select", function(e, clickedIndex, newValue, oldValue) {
    //    var selected = $(e.currentTarget).val();
    //    // The empty option is mutually exclusive with everything else and has
    //    // top priority.
    //    if (selected.indexOf('__EMPTY__') != -1) {
    //        console.log('Empty selected');
    //        $(e.currentTarget).selectpicker('deselectAll');
    //        $(e.currentTarget).selectpicker('refresh');
    //        $(e.currentTarget).val('__EMPTY__');
    //        $(e.currentTarget).selectpicker('refresh');
    //    }
    //    // The any option is mutually exclusive with everything else.
    //    else if (selected.indexOf('__ANY__') != -1) {
    //        console.log('Any selected');
    //        $(e.currentTarget).selectpicker('deselectAll');
    //        $(e.currentTarget).selectpicker('refresh');
    //        $(e.currentTarget).val('__ANY__');
    //        $(e.currentTarget).selectpicker('refresh');
    //    }
    //    console.log(e, this, 'VAL', this.value, 'SEL', selected, 'CI', clickedIndex, 'NV', newValue, 'OV', oldValue);
    //});

    $(document).on('show.bs.tab', 'a.chart-tab[data-api-url]', function (event) {
        if (event.target.search_result_data != undefined || event.target.search_active) {
            return;
        }

        event.target.search_active = true;
        $(event.target).children('.loading, .label-tag').toggleClass('hidden');

        event.target.promise = $.getJSON(event.target.getAttribute('data-api-url'), function(data) {
            event.target.search_result_data = data;

            let dict_key = event.target.getAttribute('data-dict-key');
            render_sql_queries(data, dict_key);
            render_time_marks(data, dict_key);

            let stats = data['statistics'];
            rendering_functions[dict_key].forEach(rendering_func => rendering_func(stats));
            $(event.target.getAttribute('href') + ' div.chart-toolbar').removeClass('invisible');
            event.target.search_active = false;
            $(event.target).children('.loading, .label-tag').toggleClass('hidden');
        });
    });
});

// =========================== Helper functions ===========================

function render_sql_queries(data, dict_key ) {
    if (data.sqlqueries != undefined && $(`#query_list_${dict_key}`).length) {
        let query_list = $(`#query_list_${dict_key} > ol.list-group`);
        query_list.html(''); // clear the elements inside
        query_list.append(
            data.sqlqueries.map(query => `
                <li class="list-group-item">
                    <code>${query}</code>
                </li>
            `)
        );
    } else if ($(`#query_list_${dict_key}`).length) {
        console.log("'sqlqueries' not present, skipping");
        $(`#query_list_${dict_key}`).parent().addClass('hidden');
    }
}

function ms_to_time_format(ms) {
    return new Date(ms).toISOString().slice(11, 23);
}

function render_time_marks(data, dict_key) {
    if (data.time_marks != undefined && $(`#timemark_list_${dict_key}`).length) {
        let timemark_table = $(`#timemark_list_${dict_key} > table > tbody`).first();
        timemark_table.html('');

        // can be NaN
        total_duration = new Date(data.time_marks[data.time_marks.length - 1][0]) - new Date(data.time_marks[0][0]);

        let time_mark_prev = undefined;
        let dur_ns = {};

        for (const time_mark of data.time_marks) {
            let time_difference = '';
            if (time_mark_prev != undefined) {
                time_difference = `
                    <span data-toggle="tooltip" title="${timemark_table.attr('data-title-time-difference')}${time_mark_prev[3]}:${time_mark_prev[2]}:${time_mark_prev[1]}">
                        ${ms_to_time_format(new Date(time_mark[0]) - new Date(time_mark_prev[0]))} s&nbsp;
                        ${((new Date(time_mark[0]) - new Date(time_mark_prev[0])) / total_duration).toLocaleString(undefined, {style: "percent"})}
                    </span>
                `;
            }

            let dur_key = ''
            let time_taken = ''
            if (time_mark[2] == 'end') {
                dur_key = `${time_mark[3]}:begin:${time_mark[1]}`;
                if (dur_key in dur_ns && dur_ns[dur_key] != new Date(time_mark_prev[0])) {
                    time_taken = `
                        <span data-toggle="tooltip" title="${timemark_table.attr('data-title-time-difference')}${dur_key}">
                            ${ms_to_time_format(new Date(time_mark[0]) - dur_ns[dur_key])} s&nbsp;
                            ${((new Date(time_mark[0]) - dur_ns[dur_key]) / total_duration).toLocaleString(undefined, {style: "percent"})}
                        </span>
                    `;
                }
            } else {
                dur_key = `${time_mark[3]}:${time_mark[2]}:${time_mark[1]}`
                dur_ns[dur_key] = new Date(time_mark[0]);
            }

            timemark_table.append(`
                <tr${time_mark[2] == 'end' ? ' class="bg-danger"' : ''}>
                    <td>
                        <strong>${time_mark[3]}:${time_mark[2]}:${time_mark[1]}</strong>
                    </td>
                    <td>
                        <span data-toggle="tooltip" title="${timemark_table.attr('data-title-mark-timestamp')}${time_mark[0]}">
                            <i class="fas fa-fw fa-clock"></i>&nbsp;
                        </span>
                        ${time_difference}
                    </td>
                    <td>
                        ${time_taken}
                    </td>
                    <td class="hidden-xs hidden-sm hidden-md">
                        ${time_mark[4]}
                    </td>
                </tr>
            `);

            time_mark_prev = time_mark;
        }

        $(`#total_duration_${dict_key}`).html(ms_to_time_format(total_duration));
    } else if ($(`#timemark_list_${dict_key}`).length){
        console.log("'time_marks' not present, skipping");
        $(`#timemark_list_${dict_key}`).parent().addClass('hidden')
    }
}
