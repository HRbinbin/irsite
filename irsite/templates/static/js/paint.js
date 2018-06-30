 console.log("outter")
var myChart = echarts.init(document.getElementById('chart1'));
                              option = {
                                  xAxis: {
                                      name:"Recall",
                                      type:"value",
                                      max:{{rmax}},
                              min:{{rmin}},
                              },
                              yAxis: {
                                  name:"Precision",
                                      type:"value",
                                      max:{{pmax}},
                                  min:{{pmin}},
                              },
                              series: [{
                                  data: {{pr}},
                                  type: 'line',
                                  smooth: true,
                                  symbol:"none",
                              }]
                              };
                              myChart.setOption(option)