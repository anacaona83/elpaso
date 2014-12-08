//Regular pie chart example
nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true);

    d3.select("#chart svg")
        .datum(juin2014())
        .transition().duration(350)
        .call(chart);

  return chart;
});

//Donut chart example
nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(false)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)          //Turn on Donut mode. Makes pie chart look tasty!
      .donutRatio(0.35)     //Configure how big you want the donut hole size to be.
      ;

    d3.select("#chart2 svg")
        .datum(juillet2014())
        .transition().duration(350)
        .call(chart);

  return chart;
});

//Pie chart example data. Note how there is only a single array of key-value pairs.
function juin2014() {
  return  [
      { 
        "label": "CDI",
        "value" : 12
      } , 
      { 
        "label": "CDD",
        "value" : 14
      } , 
      { 
        "label": "FPT",
        "value" : 4
      } , 
      { 
        "label": "Stage",
        "value" : 3
      } , 
      { 
        "label": "Apprentissage",
        "value" : 3
      } , 
      { 
        "label": "Mission",
        "value" : 1
      } , 
      { 
        "label": "Autre",
        "value" : 1
      }
    ];
}

function juillet2014() {
  return  [
      { 
        "label": "CDI",
        "value" : 17
      } , 
      { 
        "label": "CDD",
        "value" : 16
      } , 
      { 
        "label": "FPT",
        "value" : 2
      } , 
      { 
        "label": "Stage",
        "value" : 1
      } , 
      { 
        "label": "Apprentissage",
        "value" : 1
      } , 
      { 
        "label": "Mission",
        "value" : 2
      } , 
      { 
        "label": "Autre",
        "value" : 4
      }
    ];
}