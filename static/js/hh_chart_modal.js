$('.hh_value').click(function (event) {
    event.preventDefault();

    const $el = $(this);
    const metricId = $el.data("metric-id");
    const schoolId = $el.data("school-id");
    const page = `/high_health/chart_data/${metricId}/${schoolId}`;

    function baseDataset(data, label = null, color = null, options = {}) {
        return {
            label,
            fill: false,
            data,
            spanGaps: true,
            tension: 0,
            borderWidth: options.borderWidth || 2,
            borderDash: options.borderDash || [],
            ...(color && {
                borderColor: color,
                backgroundColor: color
            })
        };
    }

    function hasRealData(arr) {
        return Array.isArray(arr) && arr.some(v => v !== null && v !== undefined);
    }

    $.get(page)
        .done(function (response) {
            if (!response.success) return;

            const d = response.data;
            let data;
            let datasets = [];

            if (d.frequency === 'monthly') {
            datasets = [];

            // Previous year → dashed + lighter emphasis
            if (d.previous_year.length > 0) {
                datasets.push(
                    baseDataset(
                        d.previous_year,
                        d.py_label,
                        '#99999', // softer gray instead of strong color
                        {
                            borderDash: [6, 4],
                            borderWidth: 2
                        }
                    )
                );
            }

            // Current year → solid + stronger emphasis
            datasets.push(
                baseDataset(
                    d.current_year,
                    d.cy_label,
                    '#0071CE',
                    {
                        borderWidth: 3
                    }
                )
            );

            console.log(datasets);

            data = {
                labels: d.months,
                datasets: datasets
            };
        } else {
                datasets = [
                    baseDataset(d.values, null, '#0071CE')
                ];

                data = {
                    labels: d.years,
                    datasets: datasets
                };
            }

            const options = {
                title: {
                    display: true,
                    text: d.metric
                },
                legend: {
                    display: true
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            min: d.axis_min,
                            max: d.axis_max
                        }
                    }]
                },
                annotation: {
                    annotations: [{
                        type: 'line',
                        mode: 'horizontal',
                        scaleID: 'y-axis-0',
                        value: d.goal,
                        borderColor: d.goal_color,
                        borderWidth: 2,
                        label: {
                            backgroundColor: d.goal_color,
                            content: `High Health: ${d.goal_type.toLowerCase()} ${d.goal}`,
                            enabled: true
                        }
                    }]
                }
            };

            const config = {
                type: 'line',
                data: data,
                options: options
            };

            const chart_id = `chart_${metricId}_${schoolId}`;
            const ctx = document.getElementById(chart_id).getContext('2d');

            // Prevent duplicate charts on repeated clicks
            window.myCharts = window.myCharts || {};

            if (window.myCharts[chart_id]) {
                window.myCharts[chart_id].destroy();
            }

            window.myCharts[chart_id] = new Chart(ctx, config);
        })
        .fail(function () {
            console.error("Failed to load chart data:", page);
        });
});