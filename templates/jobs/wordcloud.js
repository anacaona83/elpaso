(function() {

	/* D3  */

	d3.json("../static/json/mots_geomatique.json", function(data) {
	var width = 1000;
	var height = 800;

	var typeFace = 'Impact';
	var minFontSize = 5;
	var colors = d3.scale.category20b();

	var svg = d3.select('#cloud').append('svg')
			.attr('width', width)
			.attr('height', height)
			.append('g')
			.attr('transform', 'translate('+width/2+', '+height/2+')');


	function calculateCloud(wordCount) {
		d3.layout.cloud()
			.size([width, height])
			.words((data).map(function(d) {
				return {text: d.word, size: d.size, firstime: d.firstime, lastime: d.lastime};
			}))
			/*.rotate(function() { return ~~(Math.random()*2) * 90;}) // 0 or 90deg*/
			.rotate(function(d) { return ~~(Math.random() * 5) * 30 - 60; })
			.padding(1)
			.font(typeFace)
			.fontSize(function(d) { return d.size; })
			.on('end', drawCloud)
			.start();
	}

	function drawCloud(words) {
		var vis = svg.selectAll('text').data(words);

		vis.enter().append('text')
			.style('font-size', function(d) { return d.size + 'px'; })
			.style('font-family', function(d) { return d.font; })
			.style('fill', function(d, i) { return colors(i); })
			.attr('text-anchor', 'middle')
			.attr('transform', function(d) {
			  return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
			})
			.text(function(d) { return d.text; })
			.on("click", function(d) { 
				alert(d.text + " = " + d.size + " occurrences.\nApparu la 1ère fois : " + d.firstime + "\nApparu la dernière fois : " + d.lastime);
				});
	}
		

	calculateCloud();

	})
})();