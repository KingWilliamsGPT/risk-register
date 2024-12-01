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

		var pieChart = async function(apiURL){
			//Pie chart with custom labels

			const pieChartID = '#pie-chart';

		    const res = await fetch(apiURL, {
		        headers: {
		            'X-Requested-With': 'XMLHttpRequest',
		            'Accept': 'application/json',
		        },
		        credentials: 'same-origin'  // Important for including cookies with the request
		    });
			  
			var data = {
				labels: ['35%', '55%', '10%'],
				series: [20, 15, 40]
			  };

			const draw = (data, pieChartID)=>{
				var options = {
					labelInterpolationFnc: function(value) {
					  return value[0]
					}
				  };
				  
				var responsiveOptions = [
					['screen and (min-width: 640px)', {
					  chartPadding: 30,
					  donut: true,
					  labelOffset: 100,
					  donutWidth: 60,
					  labelDirection: 'explode',
					  labelInterpolationFnc: function(value) {
						return value;
					  }
					}],
					['screen and (min-width: 1024px)', {
					  labelOffset: 60,
					  chartPadding: 20
					}]
				];
				  
				new Chartist.Pie(pieChartID, data, options, responsiveOptions);
			}

		    if (res.ok) {
		        const data = await res.json();
		        const e = $(pieChartID).parent();
		        e.removeClass('bg-loader');

		        if (!data.series.length) {
		            e.addClass('chart-area-no-data');
		            e.attr('title', 'No data was returned, try saving some data.');
		            return;
		        }

		        draw(data, pieChartID);

		    } else {
		        console.log('Failed to load risk summary bar chart data');
		        chart.innerHTML = '<p>Could not load data.</p>';
		    }
			
		}

		// var riskDeptDistribution = async function(apiURL){
			// 	/* Sample data shape
			// 		{"series":[1,1,1,5,2,2,2,1],"labels":["Environ... (1)","Financi... (1)","Market ... (1)","Operati... (5)","Politic... (2)","Reputat... (2)","Supplie... (2)","Technol... (1)"],"tooltips":["Environmental Risk","Financial Risk","Market Risk","Operational Risk","Political Risk","Reputational Risk","Supplier/Vendor Risk","Technological Risk"]}
			// 	*/

			//     const chartID = '#risk-dept-distribution';
			//     const chart = document.querySelector(chartID);

			//     const res = await fetch(apiURL, {
			//         headers: {
			//             'X-Requested-With': 'XMLHttpRequest',
			//             'Accept': 'application/json',
			//         },
			//         credentials: 'same-origin'  // Important for including cookies with the request
			//     });

			//     if (res.ok) {
			//         const data = await res.json();
			//         a = data;
			//         const e = $(chart).parent();
			//         e.removeClass('bg-loader');

			//         if (!data.series.length) {
			//             e.addClass('chart-area-no-data');
			//             e.attr('title', 'No data was returned, try saving some data.');
			//         }

			//         const chartOpt = {
			//             labelInterpolationFnc: function(value, index) {
			//                 return data.labels[index];  // Short labels for display
			//             },
			//             plugins: [
			//                 // Chartist.plugins.tooltip({
			//                 //     tooltipFnc: function(meta, value, index) {
			//                 //         return data.tooltips[index];  // Full risk type name on hover
			//                 //     }
			//                 // })
		    //                 Chartist.plugins.tooltip()  // Add tooltips (requires the Chartist tooltip plugin)

			//             ]
			//         };

			//         new Chartist.Pie(chartID, data, chartOpt);
			//     } else {
			//         console.log('Failed to load risk summary pie chart data');
			//         chart.innerHTML = '<p>Could not load data.</p>';
			//     }
		// };

		var riskDeptDistribution = async function(apiURL) {
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
		            return;
		        }

		        const chartOpt = {
		            axisX: {
		                labelInterpolationFnc: function(value, index) {
		                    return data.labels[index];  // Use short labels on the X-axis
		                }
		            },
		            plugins: [
		                Chartist.plugins.tooltip()  // Add tooltips (requires the Chartist tooltip plugin)
		            ],
		            seriesBarDistance: 10,  // Space between bars

		        };
		        

		        new Chartist.Bar(chartID, { 
		            labels: data.labels,  // X-axis labels for each bar
		            series: [data.series]  // Series data for bar heights
		        }, chartOpt)
		        .on('draw', function(data) {
		        	// possible types are grid, label and bar
					if(data.type === 'bar') {
						data.element.attr({
							style: 'stroke-width: 20px'
						});
					}
				});

		    } else {
		        console.log('Failed to load risk summary bar chart data');
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
			 select_progress_view = $('.open-risk-progress');

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

			var updateProgressChart = async (view)=>{
				const isDaily = (view == 'daily');

				const now = new Date();
				const startDate = (isDaily ? new Date(now.getTime() - (14 * 24 * 60 * 60 * 1000)) // 2 weeks
								                          : new Date(now.setMonth(now.getMonth() - 24))); // 24 months
				const endDate = new Date();

				_updateProgressChart(apiURL, startDate, endDate, view, progressChart);
			}

			select_progress_view.on('change', async (e)=>{
				// update the chart view
				const view = e.target.value; // either daily or monthly
				updateProgressChart(view);
			});


			const view = select_progress_view.find('select').val();
			updateProgressChart(view);
		}

		var riskByDepartmentDistribution = async function(apiURL) {
		     chartCanvas = document.getElementById('risk-dept-distribution2');
		    const ctx = chartCanvas.getContext('2d');

		    const res = await fetch(apiURL, {
		        headers: {
		            'X-Requested-With': 'XMLHttpRequest',
		            'Accept': 'application/json',
		        },
		        credentials: 'same-origin'
		    });

		    if (res.ok) {
		        const data = await res.json();

		        const riskDeptChart = new Chart(ctx, {
		            type: 'bar',
		            data: {
		                labels: data.labels,  // Department names
		                datasets: [
		                    {
		                        label: 'Opened Risks',
		                        data: data.open_series,
		                        backgroundColor: '#EE3232B8',
		                        borderColor: '#EE3232E8',
		                        borderWidth: 1
		                    },
		                    {
		                        label: 'Closed Risks',
		                        data: data.closed_series,
		                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
		                        borderColor: 'rgba(153, 102, 255, 1)',
		                        borderWidth: 1
		                    }
		                ]
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
		    } else {
		        console.log('Failed to load risk summary bar chart data');
		        chartCanvas.innerHTML = '<p>Could not load data.</p>';
		    }
		};



		return {
			init:function(){
			},
			
			load:function(){
				setChartWidth();	
				riskDeptDistribution(API_URLS.risk_type_summary);
				riskSuperSummaryDistribution(API_URLS.risk_super_summary);
				dailyMontlyRiskProgress(API_URLS.risk_progress);
				riskByDepartmentDistribution(API_URLS.risk_dept_summary);
				pieChart(API_URLS.risk_pie_summary_by_department);
			},
			
			resize:function(){
				pieChart(API_URLS.risk_pie_summary_by_department);
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