(function($) {
    /* "use strict" */

	function delay(s) {
		return new Promise(resolve => setTimeout(resolve, s * 1000));
	}
	

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
		var riskDeptDistribution = async function(apiURL){
			//Simple pie chart
            const chartID = '#risk-dept-distribution';
            const chart = document.querySelector(chartID);
			// await delay(4);
	
			const res = await fetch(apiURL, {
				headers: {
					'X-Requested-With': 'XMLHttpRequest',
					'Accept': 'application/json',
				},
				credentials: 'same-origin'  // This is important for including cookies with the request
			});
			
			if(res.ok){
				const data = await res.json();
				// chart.innerHTML = 'loaded data'+JSON.stringify(data);
				const chartOpt = {
					
				};
				if (!data.series.length){
					const e = $(chart).parent();
					e.removeClass('bg-loader');
					e.addClass('chart-area-no-data');
					e.attr('title', 'no data was returned, try saving some data.')
				}
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
				riskDeptDistribution(SUMMARY_BY_RISK_TYPE_API_URL);
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