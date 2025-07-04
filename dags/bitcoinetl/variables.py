from datetime import datetime

from airflow.models import Variable


def read_export_dag_vars(var_prefix, **kwargs):
    export_start_date = read_var('export_start_date', var_prefix, True, **kwargs)
    export_start_date = datetime.strptime(export_start_date, '%Y-%m-%d')

    provider_uri = read_var('provider_uri', var_prefix, True, **kwargs)

    vars = {
        'output_bucket': read_var('output_bucket', var_prefix, True, **kwargs),
        'export_start_date': export_start_date,
        'export_schedule_interval': read_var('export_schedule_interval', var_prefix, True, **kwargs),
        'provider_uri': provider_uri,
        'notification_emails': read_var('notification_emails', None, False, **kwargs),
        'export_max_active_runs': to_int(read_var('export_max_active_runs', var_prefix, False, **kwargs)),
        'export_max_workers': to_int(read_var('export_max_workers', var_prefix, True, **kwargs)),
        'export_batch_size': to_int(read_var('export_batch_size', var_prefix, True, **kwargs)),
    }

    return vars


def read_load_dag_vars(var_prefix, **kwargs):
    vars = {
        'output_bucket': read_var('output_bucket', var_prefix, True, **kwargs),
        'destination_dataset_project_id': read_var('destination_dataset_project_id', var_prefix, True, **kwargs),
        'notification_emails': read_var('notification_emails', None, False, **kwargs),
        'schedule_interval': read_var('schedule_interval', var_prefix, True, **kwargs),
        'load_all_partitions': parse_bool(read_var('load_all_partitions', var_prefix, True, **kwargs))
    }

    load_start_date = read_var('load_start_date', var_prefix, False, **kwargs)
    if load_start_date is not None:
        load_start_date = datetime.strptime(load_start_date, '%Y-%m-%d')
        vars['load_start_date'] = load_start_date

    return vars


def read_verify_streaming_dag_vars(var_prefix, **kwargs):
    vars = {
        'destination_dataset_project_id': read_var('destination_dataset_project_id', var_prefix, True, **kwargs),
        'notification_emails': read_var('notification_emails', None, False, **kwargs),
    }

    max_lag_in_minutes = read_var('max_lag_in_minutes', var_prefix, False, **kwargs)
    if max_lag_in_minutes is not None:
        vars['max_lag_in_minutes'] = max_lag_in_minutes

    return vars


def read_var(var_name, var_prefix=None, required=False, **kwargs):
    full_var_name = f'{var_prefix}{var_name}' if var_prefix is not None else var_name
    var = Variable.get(full_var_name, '')
    var = var if var != '' else None
    if var is None:
        var = kwargs.get(var_name)
    if required and var is None:
        raise ValueError(f'{full_var_name} variable is required')
    return var


def parse_bool(bool_string, default=True):
    if isinstance(bool_string, bool):
        return bool_string
    if bool_string is None or len(bool_string) == 0:
        return default
    else:
        return bool_string.lower() in ["true", "yes"]


def to_int(val):
    if val is None:
        return None
    return int(val)
