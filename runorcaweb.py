import os
os.environ["SERVER_URI"] = "http://localhost:5001"
from orcaweb import app
app.run(port=8080, debug=True)

