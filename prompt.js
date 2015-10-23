function escapeHtml(unsafe)
{
	return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;")
		 .replace(/ /g, "&nbsp;");
}

function VDU(bootmsg, address)
{
	var me = this;
	this.bootmsg = bootmsg;
	this.address = address;
	this.element = document.getElementById("vdu");
	this.reset();
	document.onkeydown = function(e) { return me.handleKeyDown(e); }
	document.onkeypress = function(e) { return me.handleKeyPress(e); }
	this.flush();
}

VDU.prototype.reset = function()
{
	var me = this;
	if (typeof this.socket !== 'undefined')
	{
		this.socket.onopen = null;
		this.socket.onmessage = null;
		this.socket.onclose = null;
	}
	this.waiting = true;
	this.history = [];
	this.commandHistory = [];
	this.html = "";
	this.input = "";
	this.bootScreen();
	this.socket_ready = false;
	this.socket = new WebSocket("ws://" + this.address);
	this.socket.onopen = function(e) { me.onconnected(); }
	this.socket.onmessage = function(e) { me.onmessage(e); }
}

VDU.prototype.debug = function(s)
{
	//document.getElementById("debug").innerHTML = s;
}

VDU.prototype.write = function(s)
{
	if (typeof s === 'undefined') s = "";
	this.history.push(s);
	this.html += escapeHtml(s) + "<br />";
}

VDU.prototype.flush = function()
{
	var s = this.html;
	if (!this.waiting)
		s += "# " + escapeHtml(this.input) + '<span class="blink">|</span>';
	this.element.innerHTML = s;
	window.scrollTo(0, document.body.scrollHeight);
}

VDU.prototype.bootScreen = function()
{
	this.write(this.bootmsg);
	this.write();
}

VDU.prototype.execute = function()
{
	var command = this.input.trim().toLowerCase();
	this.input = "";
	this.write("# " + command);
	if (command != "")
	{
		if (command == "reset")
		{
			this.reset();
		}
		else
		{
			this.commandHistory.push(command);
			this.send(command);
			//this.write("Invalid command \"" + command + "\"");
		}
	}
	this.flush();
}

VDU.prototype.handleKeyDown = function(e)
{
	if (this.waiting) return true;

	var code = e.which;
	this.debug(code);

	var handled = false;

	if (e.ctrlKey)
	{
		if (code == 85)
		{
			// ctrl-U
			this.input = "";
			handled = true;
		}
		if (code == 77)
		{
			// ctrl-M (same as CR)
			code = 13;
		}
	}
	if (code == 8)
	{
		// backspace
		if (this.input.length > 0)
		{
			this.input = this.input.substr(0, this.input.length - 1);
		}
		handled = true;
	}
	if (code == 13)
	{
		this.execute();
		handled = true;
	}
	if (code == 38)
	{
		// up arrow
		// TODO
	}
	if (handled) this.flush();
	return !handled;
}

VDU.prototype.handleKeyPress = function(e)
{
	if (this.waiting) return true;

	var code = e.which;
	this.debug(code);
	if (code >= 32 && code <= 127)
	{
		this.input += String.fromCharCode(code);
	}
	this.flush();
	return false;
}

VDU.prototype.onconnected = function()
{
	this.socket_ready = true;
	//this.write("Connection active");
	this.send("motd");
	this.flush();
}

VDU.prototype.onmessage = function(e)
{
	var data = e.data.split('\n');
	for (var i = 0; i < data.length; i++)
	{
		this.write(data[i]);
	}
	this.waiting = false;
	this.flush();
}

VDU.prototype.send = function(s)
{
	if (!this.socket_ready)
	{
		this.write("Error: cannot contact server.");
	}
	else
	{
		this.waiting = true;
		this.socket.send(s);
	}
}
