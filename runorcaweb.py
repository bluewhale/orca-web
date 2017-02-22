import os
os.environ["SERVER_URI"] = "http://orca.beta-1.linewize.net:5001"
from orcaweb import app
app.run(port=8080, debug=True)

