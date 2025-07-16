 $(document).ready(function() {
    $('#example').DataTable({
        language: {
            processing:     "Юкланяпти...",
            search:         "Қидириш:",
            lengthMenu:     "_MENU_ та қаторни кўрсатиш",
            info:           "_TOTAL_ та қатордан _START_ дан _END_ гача кўрсатилмоқда",
            infoEmpty:      "0 та қатордан 0 дан 0 гача кўрсатилмоқда",
            infoFiltered:   "(жами _MAX_ та қатордан сараланган)",
            infoPostFix:    "",
            loadingRecords: "Ёзувлар юкланмоқда...",
            zeroRecords:    "Мос келувчи қатор топилмади",
            emptyTable:     "Жадвалда маълумот мавжуд эмас",
            paginate: {
                first:      "Боши",
                previous:   "Олдинги",
                next:       "Кейингиси",
                last:       "Охири"
            },
            aria: {
                sortAscending:  ": каттадан кичикка саралаш",
                sortDescending: ": кичикдан каттага саралаш"
            }
        },
        searching: true,
        paging: true
    });
});