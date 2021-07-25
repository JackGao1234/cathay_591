import json

from bson import json_util
from flask import Flask, make_response, request
from flasgger import Swagger

from house import House
from mongo_client import MongoPipeline


mongo_pipe = MongoPipeline()
app = Flask(__name__)
swagger = Swagger(app)


@app.route('/house')
def get_houses():
    """
    This text is the description for this API.
    ---
    parameters:
    - name: "number"
      in: "query"
      description: "The phone number includes hypens. ex: 02-23753388"
      type: "string"
    - in: query
      name: gender_limit
      schema:
        type: string
      enum: [male, female, all]
      description: name of the project
    - in: query
      name: districts
      required: true
      description: A comma-separated list of districts.
      schema:
        type: array
        items:
          type: string
        minItems: 1
    responses:
      200:
        description: A list of House info
        schema:
          number:
            type: object
    """
    number = request.args.get('number')
    gender_limit = request.args.get('gender_limit')
    role = request.args.get('role')
    districts = request.args.get('districts')
    districts = districts.split(',')
    houses = mongo_pipe.get_houses(number=number, gender_limit=gender_limit, role=role, districts=districts)
    temp = []
    for h in houses:
        if len(temp) >= 1000:
            break
        temp.append(vars(House(h["id"],
                    h["district"],
                    h["name"],
                    h["role"],
                    h["phone_num"],
                    h["house_kind"],
                    h["room_kind"],
                    h["accepted_gender"])))
    return make_response(json.dumps(temp, ensure_ascii=False))


app.run(debug=True)
