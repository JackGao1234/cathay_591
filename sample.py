from flask import Flask, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/phone/<palette>/')
def colors(palette):
    """Example endpoint returning a list of phone by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of phone (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)


def get_houses(number):
    # search mongo db
    raise NotImplemented


def is_valid_phone_num(number):
    pass


@app.route('/phone/<number>/')
def phone(number):
    """Search listings by phone number
    ---
    parameters:
      - number: number
    definitions:
      number:
        type: number
    responses:
      200:
        description: A list of rent listings
    """
    if not is_valid_phone_num(number):
        return jsonify()  # return 4xx

    result = get_houses(number)

    return jsonify(result)


app.run(debug=True)
