from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<html>
<head>
<title>CYBERDECK SIGNAL TERMINAL</title>
<style>
body { background:black; color:#00ff00; font-family:monospace; }
a { color:#00ff00; display:block; margin:10px; }
</style>
</head>
<body>
<h1>VAULT SIGNAL TERMINAL</h1>

<a href="http://localhost:8073" target="_blank">[ SDR RADIO ]</a>
<a href="https://www.broadcastify.com/listen/" target="_blank">[ POLICE STREAM ]</a>
<a href="https://www.weather.gov/nwr/" target="_blank">[ NOAA WEATHER ]</a>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

app.run(host="0.0.0.0", port=5000)
