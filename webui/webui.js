var downtime = 0;
var refreshPage = function() {
		var mbstatus = null;
		try {
			var xhr = new XMLHttpRequest();
			xhr.open('GET', 'pacui.json', false);
			xhr.send(null);
			if (xhr.status == 200) {
				mbstatus = eval("(" + xhr.responseText + ")");
				downtime = 0;
			} else {
				document.getElementById('error').innerHTML = 'LIGIPÄÄSU VIGA!';
				downtime++;
			}
		} catch(e) {
			downtime++;
			document.getElementById('error').innerHTML = 'ÜHENDUSE VIGA!';
			// console.log(e, e.stack);
		}

		if (downtime > 3) {
			$('.overlay-bg').show();
		} else {
			$('.overlay-bg').hide();
		}

		if (mbstatus === null) {
			return;
		}

		// Iterate all controllers
		for (var i = 0, lni = mbstatus.device_status.length; i < lni; i ++) {
			var cname =  mbstatus.device_status[i].name;
			var caddr =  mbstatus.device_status[i].address;
			var cstatus =  mbstatus.device_status[i].status;
			var cloc = (typeof mbstatus.device_status[i].location !== 'undefined') ? mbstatus.device_status[i].location : '';
			// Register lines
			var lnj = mbstatus.device_status[i].channel_data.length;
			for (var j = 0; j < lnj; j++) {
				// Registers for one line
				for (var k = 0, lnk = mbstatus.device_status[i].channel_data[j].data.length; k < lnk; k++) {
					var rtype = mbstatus.device_status[i].channel_data[j].typename;
					var craddr = mbstatus.device_status[i].channel_data[j].data[k].address;
					if (typeof mbstatus.device_status[i].channel_data[j].data[k].bit !== 'undefined') {
						craddr += '.' + mbstatus.device_status[i].channel_data[j].data[k].bit;
					}
					var rstatus = 3;
					if (typeof mbstatus.device_status[i].channel_data[j].data[k].status !== 'undefined')
						rstatus = mbstatus.device_status[i].channel_data[j].data[k].status;
					var rvalue = mbstatus.device_status[i].channel_data[j].data[k].value;
					elem = document.getElementById(rtype + craddr);
					if (elem === null) {
						continue;
					}
					elem.innerHTML = rvalue;
					elem.innerHTML = '<div class="status' + rstatus + '">' + rvalue + '</div>';
				}
			}
		}

		// Iterate status indicators
		for (var i = 0, lni = mbstatus.modbusproxy_status.indicator.length; i < lni; i ++) {
			var iname = mbstatus.modbusproxy_status.indicator[i].name;
			var istatus = mbstatus.modbusproxy_status.indicator[i].status;
			if (iname === 'MON ON') {
				document.getElementById('mon').innerHTML = 'Monitor:<br>OK';
			}
			if (iname === 'MON OFF') {
				document.getElementById('mon').innerHTML = 'Monitor:<br>OFF';
			}
            if (iname === "VENT ?") {
				document.getElementById('vent').innerHTML = 'Vent:<br>ON';
            }
            if (iname === "VENT ON") {
				document.getElementById('vent').innerHTML = 'Vent:<br>OFF';
			}
		}

		// Iterate info
		for (var i = 0, lni = mbstatus.modbusproxy_status.info.length; i < lni; i ++) {
			if (mbstatus.modbusproxy_status.info[i].name === "WLAN IP address") {
				document.getElementById('url').innerHTML = 'URL:<br/>http://' + mbstatus.modbusproxy_status.info[i].value;
			}
			if (mbstatus.modbusproxy_status.info[i].name === "TIME") {
				document.getElementById('time').innerHTML = mbstatus.modbusproxy_status.info[i].value;
			}
		}
		document.getElementById('name').innerHTML = mbstatus.device_status[0].name;
};

refreshPage();

setInterval(function() {
	refreshPage();
}, 2000);
