


function init_socket() {
	socket = io.connect('http://' + document.domain + ':' + location.port);
};

function chart(id, data) {
	var ctx = document.getElementById(id).getContext('2d');
	var chart_config = data;
	create_chart = new Chart(ctx, chart_config);
	return create_chart
};

function chart1(id, data) {
	var ctx = document.getElementById(id).getContext('2d');
	var chart_config = data;
	create_chart1 = new Chart(ctx, chart_config);
	return create_chart1
};


function handleClick(evt) {
    var activeElement = create_chart.getElementAtEvent(evt);
		console.log(activeElement)
		console.log(activeElement)
		socket.emit('my event', activeElement[0]._chart.data.labels[activeElement[0]._index]);
		socket.on('reply', (msg) => {
			console.log(msg);
			conf = msg
		});
};

function collapse_chart() {

			chart1('chart2', JSON.parse(conf.replace(/'/g, '"')));



};



function click_labels(evt) {
	function sleep() {
		t = setTimeout(collapse_chart, 4000)
	}
	if (collapse_precise_chart.className == 'collapse') {
		handleClick(evt);
		sleep();
		$('#collapse_precise_chart').collapse('show');
	} else {
		create_chart1.destroy()
		$('#collapse_precise_chart').collapse('hide');
	}




};
