from flask import Blueprint, jsonify, render_template
from flask.helpers import flash
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError, OperationalError

bp = Blueprint('errors', __name__,
               template_folder='templates',
               static_folder='static', static_url_path='/static')

@bp.app_errorhandler(404)
def page_not_found(e):
    # return "Not found", 404
    return render_template('404.jinja'), 404

@bp.app_errorhandler(405)
def method_not_allowed(e):
    # return "Method not allowed", 405
    return jsonify({"status": "error", "result": ""}), 405

@bp.app_errorhandler(500)
def internal_server_error(e):
    # TODO: log error details etc
    return "Unexpected error", 500
    # return render_template('500.html'), 500

@bp.app_errorhandler(ValidationError)
def data_validation_error(e):
    validation_errors = e.args[0]
    return jsonify(validation_errors)

@bp.app_errorhandler(IntegrityError)
def sql_integrity_error(e):
    description = e.args[0]
    message = "Data related error occured"
    if e.orig.args[0] == 2601:
        message = "Duplicate data"
    elif e.orig.args[0] == 515:
        message = "Data is in use"

    flash(message, category="Action failed")
    return render_template("form_error.jinja")

@bp.app_errorhandler(OperationalError)
def sql_op_error(e):
    description = e.args[0]
    message = "Database related error occured"
    if e.orig.args[0][0] == 18456:
        message = "Database connection error. Try again or report problem."

    flash(message, category="Action failed")
    return render_template("form_error.jinja")
