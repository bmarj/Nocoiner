function report1ChartInit(chartDivId, caption, type='donut') {
    var options = {
        chart: {
            //width: 580,
            height: 400,
            type: type,
            foreColor: '#999999'
        },
        fill: {
            type: 'gradient',
        },
        dataLabels: {
            enabled: false
        },
        series: [],
        title: {
            text: caption,
        },
        noData: {
          text: 'Loading...'
        },
        legend: {
            formatter: function (val, opts) {
                return val + " - " + opts.w.globals.series[opts.seriesIndex]
            }
        },
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 300
                },
                legend: {
                    position: 'bottom'
                }
            }
        }]
      }
      
      let chart = new ApexCharts(
        document.querySelector(chartDivId),
        options
      );
      
      chart.render();
      return chart;
}

function updateChart(chart, json, labelColumn, valueColumn) {
    let labels = [];
    let series = [];
    let dataDict = {};

    json.data.forEach(element => {
        let prev = dataDict[element[labelColumn]] ?? 0;
        let curr = element[valueColumn];
        dataDict[element[labelColumn]] = prev + curr;
    });

    for (var key in dataDict) {
        labels.push(key);
        series.push(dataDict[key]);
    }

    var options = {
        title: chart.opts.title,
        series: series,
        chart: chart.opts.chart,
        dataLabels: {
            enabled: false
        },
        fill: chart.opts.fill,
        labels: labels,
        legend: chart.opts.legend,
        responsive: chart.opts.responsive
    };

    if (json.data.length > 100) {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: false};
    }
    else {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: true};
    }

    chart.updateOptions(options);
}


function reportAreaChartInit(chartDivId, caption, yCaption, xCaption, type='area') {

    var options = {
        chart: {
            //width: 580,
            height: 400,
            type: type,
            //foreColor: '#999999'
        },
        dataLabels: {
            enabled: false
        },
        series: [],
        title: {
            text: caption,
        },
        noData: {
          text: 'Loading...'
        },
        stroke: {
            width: 1
        },
        xaxis: {
            title: {
                text: xCaption
            },
            labels: {
                rotate: -45
            },
            //tickPlacement: 'on',
            type: "datetime",
            tickAmount: 10
        },
        yaxis: {
            title: {
                text: yCaption,
            },
        },
        fill: {
            type: 'gradient',
            opacity: 0.6
        },
        tooltip: {
            enabled: true,
            // y: {
            //     formatter: (v) => {return (v).toLocaleString('en-US', {
            //                                     style: 'currency',
            //                                     currency: 'USD',
            //                                 });
            //     }
            // },
            // z:  {
            //     //title: 'Order size',
            //     formatter: (v) => {return (v^3).toLocaleString('en-US', {
            //                                         style: 'currency',
            //                                         currency: 'USD',
            //                                     });
            //     }
            // }
        }
      }
      
      let chart = new ApexCharts(
        document.querySelector(chartDivId),
        options
      );
      
      chart.render();
      return chart;
}

function updateAreaChart(chart, json, xaxis, yaxis, sizeaxis, seriesColumn, orderedSeries=[]) {
    // extract series
    let series = orderedSeries
    if (series.length == 0)
        series = [...new Set(json.data.flatMap( (c) => { return c[seriesColumn]; }))];

    // fill data for series and each category,
    // this way will ensure that dimension of all series is the same
    let allSeries = [];
    for (s of series){
        let sData = json.data.flatMap( (c) => { return getValueForPath(c, seriesColumn)==s ? c : []; });
        let seriesData = sData.map( (c) => { return [getValueForPath(c, xaxis),
                                                    getValueForPath(c, yaxis),
                                                    //Math.abs(getValueForPath(c, sizeaxis))
                                                    // visualize it as sphere, 
                                                    Math.cbrt(Math.abs(getValueForPath(c, sizeaxis)))
                                                    ];
                                           });
        allSeries = allSeries.concat({name: s, data: seriesData});
    }

    var options = {
        title: chart.opts.title,
        chart: chart.opts.chart,
        dataLabels: {
            enabled: false
        },
        fill: chart.opts.fill,
        stroke: chart.opts.stroke,
        xaxis: chart.opts.xaxis,
        yaxis: chart.opts.yaxis,
    };

    if (json.data.length > 100) {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: false};
    }
    else {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: true};
    }

    options.series = allSeries;

    chart.updateOptions(options);
}


function reportBubbleChartInit(chartDivId, caption, yCaption, xCaption, type='bubble') {

    var options = {
        chart: {
            //width: 580,
            height: 400,
            type: type,
            foreColor: '#999999'
        },
        dataLabels: {
            enabled: false
        },
        series: [],
        title: {
            text: caption,
        },
        noData: {
          text: 'Loading...'
        },
        stroke: {
            width: 1
        },
        xaxis: {
            title: {
                text: xCaption
            },
            labels: {
                rotate: -45
            },
            //tickPlacement: 'on',
            type: "numeric",
            tickAmount: 10
        },
        yaxis: {
            title: {
                text: yCaption,
            },
        },
        fill: {
            type: 'gradient',
            opacity: 0.6
        },
        tooltip: {
            enabled: true,
            y: {
                formatter: (v) => {return (v).toLocaleString('en-US', {
                                                style: 'currency',
                                                currency: 'USD',
                                            });
                }
            },
            z:  {
                title: 'Order size',
                formatter: (v) => {return (v^3).toLocaleString('en-US', {
                                                    style: 'currency',
                                                    currency: 'USD',
                                                });
                }
            }
        }
      }
      
      let chart = new ApexCharts(
        document.querySelector(chartDivId),
        options
      );
      
      chart.render();
      return chart;
}

function updateBubbleChart(chart, json, xaxis, yaxis, sizeaxis, seriesColumn, orderedSeries=[]) {
    // extract series
    let series = orderedSeries
    if (series.length == 0)
        series = [...new Set(json.data.flatMap( (c) => { return c[seriesColumn]; }))];

    // fill data for series and each category,
    // this way will ensure that dimension of all series is the same
    let allSeries = [];
    for (s of series){
        let sData = json.data.flatMap( (c) => { return getValueForPath(c, seriesColumn)==s ? c : []; });
        let seriesData = sData.map( (c) => { return [getValueForPath(c, xaxis),
                                                    getValueForPath(c, yaxis),
                                                    //Math.abs(getValueForPath(c, sizeaxis))
                                                    // visualize it as sphere, 
                                                    Math.cbrt(Math.abs(getValueForPath(c, sizeaxis)))
                                                    ];
                                           });
        allSeries = allSeries.concat({name: s, data: seriesData});
    }

    var options = {
        title: chart.opts.title,
        chart: chart.opts.chart,
        dataLabels: {
            enabled: false
        },
        fill: chart.opts.fill,
        stroke: chart.opts.stroke,
        xaxis: chart.opts.xaxis,
        yaxis: chart.opts.yaxis,
    };

    if (json.data.length > 100) {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: false};
    }
    else {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: true};
    }

    options.series = allSeries;

    chart.updateOptions(options);
}


function reportBarChartInit(chartDivId, caption, type='bar') {
      var options = {
        chart: {
          type: type,
          stacked: true,
          parentHeightOffset: 0,
          height: 400
        },
        series: [],
        title: {
            text: caption,
        },
        // tooltip: {
        //     enabled: true,
        //     y: {
        //         formatter: (v) => {return asMoney(v);}
        //     },
        // },
        noData: {
          text: 'Loading...'
        },
        plotOptions: {
            bar: {
                columnWidth: '75%',
                endingShape: 'rounded'
            }
        },
        stroke: {
            width: 1
        },
        fill: {
            type: 'gradient',
            gradient: {
                shade: 'light',
                type: "horizontal",
                shadeIntensity: 0.25,
                gradientToColors: undefined,
                inverseColors: true,
                opacityFrom: 0.85,
                opacityTo: 0.85,
                stops: [50, 0, 100]
            },
        },
        dataLabels: {
            enabled: false
        },
      };

      let chart = new ApexCharts(
        document.querySelector(chartDivId),
        options
      );
      
      chart.render();
      return chart;
}


function updateBarChart(chart, json, xaxis, yaxis, seriesColumn, orderedSeries=[]) {
    let allSeries = []
    let labels = [...new Set(json.data.map( c => c[xaxis] ))];
    seriesNames = [...new Set(json.data.map( c => c[seriesColumn] ))];
    for (s of seriesNames){
        let seriesData = json.data.filter( c => c[seriesColumn] == s);
        let slData = [];
        for (l of labels){
            lblData = seriesData.filter(c => c[xaxis] == l).map( c => c[yaxis] );
            slData = slData.concat( arrSumFlat(lblData) );
        }
        allSeries = allSeries.concat({name: s, data: slData});
    }

    var options = {
        series: allSeries,
        xaxis: {
            categories: labels
        },
    };

    if (json.data.length > 100) {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: false};
    }
    else {
        options.chart = chart.opts.chart,
        options.chart.animations = {enabled: true};
    }

    chart.updateOptions(options);
}
