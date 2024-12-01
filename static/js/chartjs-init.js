(function($) {
    /* "use strict" */

	
	/* function draw() {
		
	} */

 var dzSparkLine = function(){
	//let draw = Chart.controllers.line.__super__.draw; //draw shadow
	
	var screenWidth = $(window).width();
	
	var pieChart = function(){
		//pie chart
		if(jQuery('#pie_chart').length > 0 ){
			//pie chart
			const pie_chart = document.getElementById("pie_chart").getContext('2d');
			// pie_chart.height = 100;
			new Chart(pie_chart, {
				type: 'pie',
				data: {
					defaultFontFamily: 'Poppins',
					datasets: [{
						data: [45, 25, 20, 10],
						borderWidth: 0, 
						backgroundColor: [
							"rgba(11, 42, 151, .9)",
							"rgba(11, 42, 151, .7)",
							"rgba(11, 42, 151, .5)",
							"rgba(0,0,0,0.07)"
						],
						hoverBackgroundColor: [
							"rgba(11, 42, 151, .9)",
							"rgba(11, 42, 151, .7)",
							"rgba(11, 42, 151, .5)",
							"rgba(0,0,0,0.07)"
						]

					}],
					labels: [
						"one",
						"two",
						"three", 
						"four"
					]
				},
				options: {
					responsive: true, 
					plugins:{
						legend:false,
						
					},
					aspectRatio:5,
					maintainAspectRatio: false
				}
			});
		}
	}
    var doughnutChart = function(){
		if(jQuery('#doughnut_chart').length > 0 ){
			//doughut chart
			const doughnut_chart = document.getElementById("doughnut_chart").getContext('2d');
			// doughnut_chart.height = 100;
			new Chart(doughnut_chart, {
				type: 'doughnut',
				data: {
					weight: 5,	
					defaultFontFamily: 'Poppins',
					datasets: [{
						data: [45, 25, 20],
						borderWidth: 3, 
						borderColor: "rgba(255,255,255,1)",
						backgroundColor: [
							"rgba(11, 42, 151, 1)",
							"rgba(39, 188, 72, 1)",
							"rgba(139, 199, 64, 1)"
						],
						hoverBackgroundColor: [
							"rgba(11, 42, 151, 0.9)",
							"rgba(39, 188, 72, .9)",
							"rgba(139, 199, 64, .9)"
						]

					}],
				},
				options: {
					weight: 1,	
					cutout: 30,
					responsive: true,
					maintainAspectRatio: false
				}
			});
		}
	}



	/* Function ============ */
		return {
			init:function(){
			},
			
			
			load:function(){
				barChart1();	
				barChart2();
				barChart3();	
				lineChart1();	
				lineChart2();		
				lineChart3();
				lineChart03();
				areaChart1();
				areaChart2();
				areaChart3();
				radarChart();
				pieChart();
				doughnutChart(); 
				polarChart(); 
			},
			
			resize:function(){
				barChart1();	
				barChart2();
				barChart3();	
				lineChart1();	
				lineChart2();		
				lineChart3();
				lineChart03();
				areaChart1();
				areaChart2();
				areaChart3();
				radarChart();
				pieChart();
				doughnutChart(); 
				polarChart(); 
			}
		}
	
	}();

	jQuery(document).ready(function(){
	});
		
	jQuery(window).on('load',function(){
		dzSparkLine.load();
	});

	jQuery(window).on('resize',function(){
		//dzSparkLine.resize();
		setTimeout(function(){ dzSparkLine.resize(); }, 1000);
	}); 
	
})(jQuery);