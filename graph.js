var DateTime = luxon.DateTime;

const ctx = document.getElementById('temp_graph').getContext('2d');

Chart.overrides.line.pointRadius = 0;
Chart.overrides.line.cubicInterpolationMode = 'monotone';
Chart.defaults.interaction.mode = 'index';
Chart.defaults.interaction.intersect = false;


const temp_graph = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [
            {
                label: "Température intérieure",
                borderColor: '#ff6368',
                backgroundColor: '#ff6368',
                data: temperatures,
                parsing: {
                    xAxisKey: 'date',
                    yAxisKey: 'in1',
                },
                xAxisID: 'x',
                yAxisID: 'int',
            },
            {
                label: "Température intérieure Phil",
                borderColor: '#ff6368',
                backgroundColor: '#ff6368',
                data: temperatures,
                borderDash: [5, 5],

                parsing: {
                    xAxisKey: 'date',
                    yAxisKey: 'in2',
                },
                xAxisID: 'x',
                yAxisID: 'int',
            },
            {
                label: "Température extérieure",
                borderColor: '#3080d0',
                backgroundColor: '#3080d0',
                data: temperatures,
                parsing: {
                    xAxisKey: 'date',
                    yAxisKey: 'ex1',
                },
                xAxisID: 'x',
                yAxisID: 'ext',
            },
            {
                label: "Température extérieure Phil",
                borderColor: '#3080d0',
                backgroundColor: '#3080d0',
                data: temperatures,
                borderDash: [5, 5],
                parsing: {
                    xAxisKey: 'date',
                    yAxisKey: 'ex2',
                },
                xAxisID: 'x',
                yAxisID: 'ext',
            }]
    },
    options: {
        events:['click', 'touchstart'],
        scales: {
            x: {
                type: 'time',
                adapters: {date: {locale: "fr"}},
                time: {
                    displayFormats: {hour: "EEE H'h'"}
                },
                ticks: {
                    color: function (ctx) {
                        let date = DateTime.fromMillis(ctx.tick.value);
                        if (date.hour < 8 || date.hour > 19)
                            return 'gray'
                        return 'orange';
                    }
                }
            },
            int: {
                type: 'linear',
                position: 'left',
                ticks: {
                    color: '#ff6368',
                },
                title: {
                    display: true,
                    text: "Température intérieure",
                },
            },
            ext: {
                type: 'linear',
                position: 'right',
                ticks: {
                    color: '#3080d0',
                },
                title: {
                    display: true,
                    text: "Température extérieure",
                },
            }
        }
    }
});
