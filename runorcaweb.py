import os
os.environ["SERVER_URI"] = "http://ec2-52-53-247-58.us-west-1.compute.amazonaws.com:5001"
from orcaweb import app
app.run(port=8080, debug=True)

