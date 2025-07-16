$(function () {
    const Calendar = FullCalendar.Calendar;
    const Draggable = FullCalendar.Draggable;
    console.log(Calendar)
    const containerEl = document.getElementById('external-events');
    const checkbox = document.getElementById('drop-remove');
    const calendarEl = document.getElementById('calendar');

    // initialize the external events
    // -----------------------------------------------------------------

    new Draggable(containerEl, {
        itemSelector: '.external-event',
        eventData: function (eventEl) {
            return {
                title: eventEl.innerText,
                backgroundColor: window.getComputedStyle(eventEl, null).getPropertyValue('background-color'),
                borderColor: window.getComputedStyle(eventEl, null).getPropertyValue('background-color'),
                textColor: window.getComputedStyle(eventEl, null).getPropertyValue('color'),
            };
        }
    });

    function addEvent(title, start, end) {
        $.ajax({
            type: "GET",
            url: '/add_event',
            data: {title, start, end},
            dataType: "json",
            error: function (data) {
                alert('There is a problem!!!');
            }
        });
    }

    function addDuty(user_id, start, end) {
        $.ajax({
            type: "GET",
            url: '/add_duty',
            data: {user_id, start, end},
            dataType: "json",
            error: function (data) {
                alert('There is a problem!!!');
            }
        });
    }

    function update(id, start, end, model) {
        $.ajax({
            type: "GET",
            url: '/update',
            data: {id, start, end, model},
            dataType: "json",
            success: function (data) {
                calendar.refetchEvents()
                console.log('Event Update');
            },
            error: function (data) {
                console.log('There is a problem!!!');
            }
        });
    }

    const calendar = new Calendar(calendarEl, {
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: function (info, successCallback, failureCallback) {
            let res = []
            $.get('/all_events', (data, status) => {
                successCallback(data.map(event =>
                    ({
                        id: event.id,
                        title: event.title,
                        url: '/' + event.model + '/edit/' + event.id,
                        end: event.end,
                        start: event.start,
                        color: event.color,
                        model: event.model
                    })))
            })
        },
        selectable: true,
        selectHelper: true,
        editable: true,
        droppable: true, // this allows things to be dropped onto the calendar
        drop: function (info) {
            console.log(info)
            const user_id = info.draggedEl.dataset.userId;
            const startStr = info.dateStr;
            const endStr = moment(info.date).add(1, 'days').format('Y-MM-DD');
            addDuty(user_id, startStr, endStr)
            calendar.refetchEvents()

            // is the "remove after drop" checkbox checked?
            if (checkbox?.checked) {
                // if so, remove the element from the "Draggable Events" list
                info.draggedEl.parentNode.removeChild(info.draggedEl);
            }
        },

        select: function (date) {
            $('#myModal').modal('show')
            // if (title) {
            //     addEvent(title, date.startStr, date.endStr);
            //     calendar.refetchEvents()
            // }
        },
        eventResize: function (_event) {
            const event = _event.event
            const start = moment(event.start).format('YYYY-MM-DD');
            const end = moment(event.end).format('YYYY-MM-DD');
            const id = event.id;
            const model = _event.event.extendedProps.model;
            update(id, start, end, model);
        },

        eventDrop: function (_event) {
            console.log(_event)
            const event = _event.event
            const start = moment(event.start).format('YYYY-MM-DD');
            const end = moment(event.end).format('YYYY-MM-DD');
            const id = event.id;
            const model = _event.event.extendedProps.model;
            update(id, start, end, model);
        },

        eventClick: function (_event) {
            new Tooltip(_event.el, {
                title: _event.event.title,
                placement: 'top',
                trigger: 'hover',
                container: 'body'
            });
        },
    });

    calendar.render();
    // $('#calendar').fullCalendar()

    /* ADDING EVENTS */
    let currColor = '#3c8dbc'; //Red by default
    // Color chooser button
    $('#color-chooser > li > a').click(function (e) {
        e.preventDefault()
        // Save color
        currColor = $(this).css('color')
        // Add color effect to button
        $('#add-new-event').css({
            'background-color': currColor,
            'border-color': currColor
        })
    })
    $('#add-new-event').click(function (e) {
        e.preventDefault()
        // Get value and make sure it is not null
        const val = $('#new-event').val();
        if (val.length == 0) {
            return
        }

        // Create events
        const event = $('<div />');
        event.css({
            'background-color': currColor,
            'border-color': currColor,
            'color': '#fff'
        }).addClass('external-event')
        event.text(val)
        $('#external-events').prepend(event)

        // Add draggable funtionality
        ini_events(event)

        // Remove event from text input
        $('#new-event').val('')
    })
})
