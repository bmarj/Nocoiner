from flask import Blueprint, jsonify, render_template
from marshmallow.exceptions import ValidationError

errors = Blueprint('errors', __name__,
                   template_folder='templates',
                   static_folder='static', static_url_path='/static')

@errors.app_errorhandler(404)
def page_not_found(e):
    #return "Not found", 404
    return render_template('404.jinja'), 404

@errors.app_errorhandler(500)
def internal_server_error(e):
    # TODO: log error details etc
    return "Unexpected error", 500
    # return render_template('500.html'), 500

@errors.app_errorhandler(ValidationError)
def data_validation_error(e):
    validation_errors = e.args[0]
    return jsonify(validation_errors)
