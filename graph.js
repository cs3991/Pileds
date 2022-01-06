var DateTime = luxon.DateTime;

const ctx = document.getElementById('temp_graph').getContext('2d');

Chart.overrides.line.pointRadius = 0;
Chart.overrides.line.cubicInterpolationMode = 'monotone';
Chart.defaults.interaction.mode = 'index';
Chart.defaults.interaction.intersect = false;


const temp_graph = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: "Température intérieure",
            borderColor: 'red',
            backgroundColor: 'red',
            data: temperatures,
            parsing: {
                xAxisKey: 'date',
                yAxisKey: 'Temperature_int',
            },
            xAxisID: 'x',
            yAxisID: 'int',
        }, 
        {
            label: "Température extérieure",
            borderColor: 'blue',
            backgroundColor: 'blue',
            data: temperatures,
            parsing: {
                xAxisKey: 'date',
                yAxisKey: 'Temperature_ext',
            },
            xAxisID: 'x',
            yAxisID: 'ext',
        }]
    },
    options: {
        scales: {
          x: {
            type: 'time',
            adapters: {date: { locale: "fr" }},
            time: {
                displayFormats: {hour: "EEE H'h'"}
            },
            ticks: {
                color: function(ctx) {
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
                color: 'red',
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
                color: 'blue',
            },
            title: {
                display: true,
                text: "Température extérieure",
            },
          }
        }
      }
    });
