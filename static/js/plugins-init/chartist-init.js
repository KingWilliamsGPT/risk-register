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
		    const chartID = '#risk-dept-distribution';
		    const chart = document.querySelector(chartID);

		    const res = await fetch(apiURL, {
		        headers: {
		            'X-Requested-With': 'XMLHttpRequest',
		            'Accept': 'application/json',
		        },
		        credentials: 'same-origin'  // Important for including cookies with the request
		    });

		    if (res.ok) {
		        const data = await res.json();
		        const e = $(chart).parent();
		        e.removeClass('bg-loader');

		        if (!data.series.length) {
		            e.addClass('chart-area-no-data');
		            e.attr('title', 'No data was returned, try saving some data.');
		        }

		        const chartOpt = {
		            labelInterpolationFnc: function(value, index) {
		                return data.labels[index];  // Short labels for display
		            },
		            plugins: [
		                // Chartist.plugins.tooltip({
		                //     tooltipFnc: function(meta, value, index) {
		                //         return data.tooltips[index];  // Full risk type name on hover
		                //     }
		                // })
	                    Chartist.plugins.tooltip()  // Add tooltips (requires the Chartist tooltip plugin)

		            ]
		        };

		        new Chartist.Pie(chartID, data, chartOpt);
		    } else {
		        console.log('Failed to load risk summary pie chart data');
		        chart.innerHTML = '<p>Could not load data.</p>';
		    }
		};

		var riskSuperSummaryDistribution = async function(apiURL){
		     risk_opened = $('#risk_opened');
		     risk_closed = $('#risk_closed');
		     risk_budget_opened = $('#risk_budget_opened');

		    const res = await fetch(apiURL, {
		        headers: {
		            'X-Requested-With': 'XMLHttpRequest',
		            'Accept': 'application/json',
		        },
		        credentials: 'same-origin'  // Important for including cookies with the request
		    });

		    if (res.ok) {
		        const data = await res.json();
		        console.log(data);
		        risk_opened.text(data.opened_risks);
		        risk_closed.text(data.closed_risks);
		        risk_budget_opened.text(data.budget_for_opened_risks);
		    } else {
		        console.log('Failed to load data');
		    }
		};

		return {
			init:function(){
			},
			
			load:function(){
				setChartWidth();	
				riskDeptDistribution(API_URLS.risk_type_summary);
				riskSuperSummaryDistribution(API_URLS.risk_super_summary);
			},
			
			resize:function(){
			}
		}
	
		var riskSevereSummaryDistribution = async function(apiURL){
		     risk_opened = $('#risk_opened');
		     risk_closed = $('#risk_closed');
		     risk_budget_opened = $('#risk_budget_opened');

		    const res = await fetch(apiURL, {
		        headers: {
		            'X-Requested-With': 'XMLHttpRequest',
		            'Accept': 'application/json',
		        },
		        credentials: 'same-origin'  // Important for including cookies with the request
		    });

		    if (res.ok) {
		        const data = await res.json();
		        console.log(data);
		        risk_opened.text(data.opened_risks);
		        risk_closed.text(data.closed_risks);
		        risk_budget_opened.text(data.budget_for_opened_risks);
		    } else {
		        console.log('Failed to load data');
		    }
		};

		return {
			init:function(){
			},
			
			load:function(){
				setChartWidth();	
				riskDeptDistribution(API_URLS.risk_type_summary);
				riskSuperSummaryDistribution(API_URLS.risk_super_summary);
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