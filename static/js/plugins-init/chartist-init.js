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
		    const risk_opened = $('#risk_opened');
		    const risk_closed = $('#risk_closed');
		    const risk_budget_opened = $('#risk_budget_opened');

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

		var dailyMontlyRiskProgress = async function(apiURL){
			const e_id = '#daily-montly-risk-progress';
			const elem = $(e_id);
			const barWidth = 50;

			var data = {
				labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec','Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',],
				series: [
				  [5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8,5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8,5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8,],
				  [3, 2, 9, 5, 4, 6, 4, 6, 7, 8, 7, 4,5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8,5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8,]
				]
			  };

			var options = {
				seriesBarDistance: 10
			};

			const chartWidth = data.labels.length * barWidth;
			elem.css({width: chartWidth + 'px'});

			var responsiveOptions = [
				['screen and (max-width: 640px)', {
				  seriesBarDistance: 5,
				  axisX: {
					labelInterpolationFnc: function (value) {
					  return value[0];
					}
				  }
				}]
			];
			new Chartist.Bar(e_id, data, options, responsiveOptions);
		}


		var _updateProgressChart = async function(apiURL, startDate, endDate, view, progressChart) {
		    startDate = startDate.toISOString();
		    endDate = endDate.toISOString();

		    const url = `${apiURL}?view=${view}&startDate=${startDate}&endDate=${endDate}`;

		    try {
		        const res = await fetch(url, {
		            headers: {
		                'X-Requested-With': 'XMLHttpRequest',
		                'Accept': 'application/json',
		            },
		            credentials: 'same-origin'  // Important for including cookies with the request
		        });

		        if (res.ok) {
		            const data = await res.json();
		            progressChart.data.datasets[0].data = data.opened_risks || [];
		            progressChart.data.datasets[1].data = data.closed_risks || [];
		            progressChart.data.labels = data.labels || [];
		            progressChart.update();
		        } else {
		            console.log(`Failed to load data for view ${view}`);
		        }
		    } catch (error) {
		        console.error(`Error fetching data for view ${view}:`, error);
		    }
		}

		var dailyMontlyRiskProgress = async function(apiURL){
			const select_progress_view = $('.open-risk-progress');

			const chartCanvas = document.getElementById('daily-montly-risk-progress');
			const ctx = chartCanvas.getContext('2d');
			const progressChart = new Chart(ctx, {
			    type: 'bar',
			    data: {
			        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
			                 'Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
			        datasets: [{
			            label: 'Opened Risks',
			            data: [5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8, 5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8, 5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8],
			            backgroundColor: '#EE3232B8',
			            borderColor: '#EE3232E8',
			            borderWidth: 1
			        }, {
			            label: 'Closed Risks',
			            data: [3, 2, 9, 5, 4, 6, 4, 6, 7, 8, 7, 4, 5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8, 5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8],
			            backgroundColor: 'rgba(153, 102, 255, 0.2)',
			            borderColor: 'rgba(153, 102, 255, 1)',
			            borderWidth: 1
			        }]
			    },
			    options: {
			        responsive: true,
			        maintainAspectRatio: false,
			        scales: {
			            x: {
			                beginAtZero: true
			            },
			            y: {
			                beginAtZero: true
			            }
			        }
			    }
			});

			select_progress_view.on('change', async (e)=>{
				// update the chart view
				const view = e.target.value; // either daily or monthly
				const isDaily = (view == 'daily');

				const now = new Date();
				const startDate = (isDaily ? new Date(now.getTime() - (14 * 24 * 60 * 60 * 1000)) // 2 weeks
								                          : new Date(now.setMonth(now.getMonth() - 24))); // 24 months
				const endDate = now;

				_updateProgressChart(apiURL, startDate, endDate, view, progressChart);

			});
		}


		return {
			init:function(){
			},
			
			load:function(){
				setChartWidth();	
				riskDeptDistribution(API_URLS.risk_type_summary);
				riskSuperSummaryDistribution(API_URLS.risk_super_summary);
				dailyMontlyRiskProgress(API_URLS.risk_progress);
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