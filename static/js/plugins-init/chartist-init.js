(function($) {
    /* "use strict" */


	var dzChartlist = function(){
		
		var screenWidth = $(window).width();
			
		var setChartWidth = function(){
			
			if(screenWidth <= 768)
			{
				var chartBlockWidth = 0;
				if(screenWidth >= 500)
				{
					chartBlockWidth = 250;
				}else{
					chartBlockWidth = 300;
				}
				
				jQuery('.chartlist-chart').css('min-width',chartBlockWidth - 31);
			}
		}
		var riskDeptDistribution = async function(){
			//Simple pie chart
            const chartID = '#risk-dept-distribution';
            const chart = document.querySelector(chartID);
	
			const res = await fetch(apiURL, {
				headers: {
					'X-Requested-With': 'XMLHttpRequest',
					'Accept': 'application/json',
				},
				credentials: 'same-origin'  // This is important for including cookies with the request
			});
			
			if(res.ok){
				 data = await res.json();
				// chart.innerHTML = 'loaded data'+JSON.stringify(data);
				const chartOpt = {};
				
				new Chartist.Pie(chartID, data, chartOpt);
			}else{
				console.log('failed to load risk summary pie chart data');
				chart.innerHTML =  '<p>Could not load data.</p>'
			}
			
		}

		return {
			init:function(){
			},
			
			load:function(){
				setChartWidth();	
				riskDeptDistribution();
			},
			
			resize:function(){
			}
		}
	
	}();

	jQuery(document).ready(function(){
	});
		
	jQuery(window).on('load',function(){
		dzChartlist.load();
	});

	jQuery(window).on('resize',function(){
		dzChartlist.resize();
	});     

})(jQuery);