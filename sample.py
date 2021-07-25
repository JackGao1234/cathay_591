import json

from bson import json_util
from flask import Flask, jsonify, Response, make_response
from flasgger import Swagger

from house import House
from settings import MongoPipeline


def parse_json(data):
    return json.loads(json_util.dumps(data))

mongo_pipe = MongoPipeline()
app = Flask(__name__)
swagger = Swagger(app)


@app.route('/phone_num/<number>/')
def get_houses(number):
    """
    This text is the description for this API.
    ---
    parameters:
    - name: "number"
      in: "path"
      description: "The phone number includes hypens. ex: 02-23753388"
      required: true
      type: "string"
    responses:
      200:
        description: A list of House info
        schema:
          number:
            type: object
    """
    houses = mongo_pipe.get_houses(number)
    temp = []
    for h in houses:
        temp.append(vars(House(h["id"],
                    h["district"],
                    h["name"],
                    h["role"],
                    h["phone_num"],
                    h["house_kind"],
                    h["room_kind"],
                    h["accepted_gender"])))
    return make_response(json.dumps(temp,ensure_ascii=False))


app.run(debug=True)
