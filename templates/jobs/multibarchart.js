nv.addGraph(function() {
  var chart = nv.models.multiBarChart()
                .x(function(d) { return d[0] })
                .y(function(d) { return d[1] })
                ;
 
  
  chart.xAxis
      .showMaxMin(false)
      .tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });

  chart.yAxis
      .tickFormat(d3.format(',.0f'));

  d3.select('#chart svg')
    .datum(data)
      .transition().duration(500).call(chart);

  nv.utils.windowResize(chart.update);

  return chart;
});