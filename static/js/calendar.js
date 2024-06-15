$(function () {
    const Calendar = FullCalendar.Calendar;
    const Draggable = FullCalendar.Draggable;

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

    function updateDuty(id, start, end) {
        $.ajax({
            type: "GET",
            url: '/update_duty',
            data: {id, start, end},
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
            $.get('/all_duties', (data, status) => {
                res = res.concat(data.map(duty => ({
                    id: duty.id,
                    title: duty.title,
                    end: duty.end,
                    start: duty.start,
                    color: duty.color,
                    duty: true
                })))
                $.get('/all_tickets', (data, status) => {
                    res = res.concat(data.map(duty => ({
                        id: duty.id,
                        title: duty.title,
                        end: duty.end,
                        start: duty.start,
                        color: duty.color,
                        ticket: true
                    })))
                    successCallback(res)
                })
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
            if (checkbox.checked) {
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
            updateDuty(id, start, end);
        },

        eventDrop: function (_event) {
            console.log(_event)
            const event = _event.event
            const start = moment(event.start).format('YYYY-MM-DD');
            const end = moment(event.end).format('YYYY-MM-DD');
            const id = event.id;
            updateDuty(id, start, end);
        },

        eventClick: function (_event) {
            console.log('Event', _event)
            if (confirm("Are you sure you want to remove it?")) {
                const id = _event.event.id;
                const ticket = _event.event.extendedProps.ticket;
                const duty = _event.event.extendedProps.duty;
                $.ajax({
                    type: "GET",
                    url: '/remove',
                    data: {'id': id, ticket, duty},
                    dataType: "json",
                    success: function (data) {
                        calendar.refetchEvents()
                    },
                    error: function (data) {
                        alert('There is a problem!!!');
                    }
                });
            }
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
