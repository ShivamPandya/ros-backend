import uuid
import base64
import json
from flask import jsonify, make_response
from flask_restful import abort
import ast as type_evaluation
from ros.lib.models import RhAccount, System, db


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val), version=4)
        return True
    except ValueError:
        return False


def get_or_create(session, model, keys, **kwargs):
    if not keys:
        keys = kwargs.keys()
    if isinstance(keys, str):
        keys = [keys]
    if not isinstance(keys, list):
        raise TypeError('keys argument must be a list or string')
    instance = session.query(model).filter_by(**{k: kwargs[k] for k in keys}).first()
    if instance:
        for k, v in kwargs.items():
            setattr(instance, k, v)
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
    return instance


def delete_record(session, model, **kwargs):
    """ Deletes a record filtered by key(s) present in kwargs(contains model specific fields)."""
    keys = list(kwargs.keys())
    instance = session.query(model).filter_by(**{k: kwargs[k] for k in keys}).first()
    if instance:
        session.delete(instance)
        session.commit()
    return instance


def identity(request):
    ident = request.headers.get('X-RH-IDENTITY')
    if not ident:
        response = make_response(
            jsonify({"Error": "Authentication token not provided"}), 401)
        abort(response)
    else:
        return json.loads(base64.b64decode(ident))


def user_data_from_identity(identity):
    """
    Get the user details dict from the rh-identity data or error out.
    """
    if 'user' not in identity:
        return None

    return identity['user']


def validate_type(value, type_):
    """
    Validate the type of a value.
    Currently available types: bool
    :param value: Value to validate.
    :param type_: Type to validate against.
    :return: True if the value is of the specified type, False otherwise.
    """
    if type_ == bool:
        # ast.literal_eval does not understand lowercase 'True' or 'False'
        value = value.capitalize() if value in ['true', 'false'] else value
    evaluated_value = type_evaluation.literal_eval(value) if value else None

    return True if type(evaluated_value) == type_ else False


def cast_iops_as_float(iops_all_dict):
    """
    Convert IOPS  values from str to float
    :param iops_all_dict: IOPS dict to convert.
    :return: IOPS values as float
    """
    iops_all_dict_float = {}
    for key, value in iops_all_dict.items():
        try:
            iops_all_dict_float[key] = float(value)
        except ValueError:
            continue
    return iops_all_dict_float


def sort_io_dict(performance_utilization: dict):
    """
    Sorts io dict by max_io in descending order.
    """
    sorted_io_dict = {
        'io_all': dict(sorted(performance_utilization['io'].items(), key=lambda x: x[1], reverse=True))
    }
    performance_utilization.update({**sorted_io_dict})
    del performance_utilization['io']
    return performance_utilization


def system_ids_by_account(account_number):
    account_query = db.session.query(RhAccount.id).filter(RhAccount.account == account_number).subquery()
    return db.session.query(System.id).filter(System.account_id.in_(account_query))
