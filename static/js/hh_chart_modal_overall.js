$('.hh_value').click(function (event) {
    event.preventDefault();
    var metric_id = $(this).attr("data-metric-id");
    var school_id = $(this).attr("data-school-id");
    $.get("/high_health/chart_data_overall/" + metric_id + "/" + school_id, function (response) {
        if (response['success']) {
            var data = {
                labels: response['data']['months'],
                datasets: [{
                    label: response['data']['py_label'],
                    fill: false,
                    data: response['data']['previous_year'],
                }, {
                    label: response['data']['cy_label'],
                    fill: false,
                    borderColor: '#0071CE',
                    backgroundColor: '#0071CE',
                    data: response['data']['current_year'],
                }]
            }
            var options = {
                title: {
                    display: true,
                    text: response['data']['metric']
                },
                scales: {
                    yAxes: [{
                        display: true,
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                },
                annotation: {
                    annotations: [{
                        type: 'line',
                        mode: 'horizontal',
                        scaleID: 'y-axis-0',
                        value: response['data']['goal'],
                        borderColor: '#6CC04A',
                        borderWidth: 2,
                        label: {
                            backgroundColor: '#6CC04A',
                            content: 'Goal: ' + response['data']['goal'],
                            enabled: true
                        }
                    }]
                }
            }
            var config = {
                type: 'line',
                data: data,
                options: options
            }
            var chart_id = 'chart_' + metric_id + '_' + school_id;
            var ctx = document.getElementById(chart_id).getContext('2d');
            var myChart = new Chart(ctx, config);
        }
    });
});