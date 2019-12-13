$('.hh_value').click(function (event) {
    event.preventDefault();
    var metric_id = $(this).attr("data-metric-id");
    var school_id = $(this).attr("data-school-id");
    var page = "/high_health/chart_data/" + metric_id + "/" + school_id
    $.get(page, function (response) {
        if (response['success']) {
            if (response['data']['frequency'] == 'monthly') {
                var data = {
                    labels: response['data']['months'],
                    datasets: [{
                        label: response['data']['py_label'],
                        fill: false,
                        data: response['data']['previous_year'],
                        lineTension: 0,
                    }, {
                        label: response['data']['cy_label'],
                        fill: false,
                        borderColor: '#0071CE',
                        backgroundColor: '#0071CE',
                        data: response['data']['current_year'],
                        lineTension: 0,
                    }]
                }
            } else {
                var data = {
                    labels: response['data']['years'],
                    datasets: [{
                        fill: false,
                        borderColor: '#0071CE',
                        backgroundColor: '#0071CE',
                        data: response['data']['values'],
                        lineTension: 0,
                    }]
                }
            }
            var options = {
                title: {
                    display: true,
                    text: response['data']['metric']
                },
                legend: {
                    display: response['data']['frequency'] == 'monthly' ? true : false
                },
                scales: {
                    yAxes: [{
                        display: true,
                        ticks: {
                            min: response['data']['axis_min'],
                            max: response['data']['axis_max'],
                        }
                    }]
                },
                annotation: {
                    annotations: [{
                        type: 'line',
                        mode: 'horizontal',
                        scaleID: 'y-axis-0',
                        value: response['data']['goal'],
                        borderColor: response['data']['goal_color'],
                        borderWidth: 2,
                        label: {
                            backgroundColor: response['data']['goal_color'],
                            content: 'Goal: ' + response['data']['goal_type'].toLowerCase() + ' ' + response['data']['goal'],
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
    $.ajax({
        data: { 'page': window.location.origin + page },
        type: 'POST',
        url: '/pageview/',
    });
});