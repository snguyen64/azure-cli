# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=unused-argument
from knack.util import CLIError, to_snake_case

from azure.cli.core.cloud import (Cloud,
                                  get_clouds,
                                  get_cloud,
                                  remove_cloud,
                                  add_cloud,
                                  _get_cloud_name,
                                  switch_active_cloud,
                                  update_cloud,
                                  get_active_cloud_name,
                                  cloud_is_registered,
                                  CloudAlreadyRegisteredException,
                                  CloudNotRegisteredException,
                                  CannotUnregisterCloudException)


def list_clouds(cmd):
    return get_clouds(cmd.cli_ctx)


def show_cloud(cmd, cloud_name=None):
    if not cloud_name:
        cloud_name = cmd.cli_ctx.cloud.name
    try:
        return get_cloud(cmd.cli_ctx, cloud_name)
    except CloudNotRegisteredException as e:
        raise CLIError(e)


def _populate_from_metadata_endpoint(cloud, arm_endpoint, session=None):
    endpoints_in_metadata = ['active_directory_graph_resource_id',
                             'active_directory_resource_id', 'active_directory']
    METADATA_ENDPOINT_SUFFIX = '/metadata/endpoints?api-version=2015-01-01'
    if not arm_endpoint or all([cloud.endpoints.has_endpoint_set(n) for n in endpoints_in_metadata]):  # pylint: disable=use-a-generator
        return
    import requests
    error_msg_fmt = "Unable to get endpoints from the cloud.\n{}"
    try:
        session = requests.Session() if session is None else session
        metadata_endpoint = arm_endpoint + METADATA_ENDPOINT_SUFFIX
        response = session.get(metadata_endpoint)
        if response.status_code == 200:
            metadata = response.json()
            if not cloud.endpoints.has_endpoint_set('gallery'):
                setattr(cloud.endpoints, 'gallery', metadata.get('galleryEndpoint'))
            if not cloud.endpoints.has_endpoint_set('active_directory_graph_resource_id'):
                setattr(cloud.endpoints, 'active_directory_graph_resource_id', metadata.get('graphEndpoint'))
            if not cloud.endpoints.has_endpoint_set('active_directory'):
                setattr(cloud.endpoints, 'active_directory', metadata['authentication'].get('loginEndpoint'))
            if not cloud.endpoints.has_endpoint_set('active_directory_resource_id'):
                setattr(cloud.endpoints, 'active_directory_resource_id', metadata['authentication']['audiences'][0])
        else:
            msg = 'Server returned status code {} for {}'.format(response.status_code, metadata_endpoint)
            raise CLIError(error_msg_fmt.format(msg))
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as err:
        msg = 'Please ensure you have network connection. Error detail: {}'.format(str(err))
        raise CLIError(error_msg_fmt.format(msg))
    except ValueError as err:
        msg = 'Response body does not contain valid json. Error detail: {}'.format(str(err))
        raise CLIError(error_msg_fmt.format(msg))


def _build_cloud(cli_ctx, cloud_name, cloud_config=None, is_update=False, cloud_args=None):
    from azure.cli.core.cloud import CloudEndpointNotSetException
    if cloud_config:
        # Using JSON format so convert the keys to snake case
        cloud_args = {to_snake_case(k): v for k, v in cloud_config.items()}
    c = Cloud(cloud_name)
    c.profile = cloud_args.get('profile', None)
    try:
        endpoints = cloud_args['endpoints']
        for arg in endpoints:
            setattr(c.endpoints, to_snake_case(arg), endpoints[arg])
    except KeyError:
        pass
    try:
        suffixes = cloud_args['suffixes']
        for arg in suffixes:
            setattr(c.suffixes, to_snake_case(arg), suffixes[arg])
    except KeyError:
        pass

    for arg in cloud_args:
        if arg.startswith('endpoint_') and cloud_args[arg] is not None:
            setattr(c.endpoints, arg.replace('endpoint_', ''), cloud_args[arg])
        elif arg.startswith('suffix_') and cloud_args[arg] is not None:
            setattr(c.suffixes, arg.replace('suffix_', ''), cloud_args[arg])

    try:
        arm_endpoint = c.endpoints.resource_manager
    except CloudEndpointNotSetException:
        arm_endpoint = None

    from azure.cli.core.breaking_change import print_conditional_breaking_change
    if arm_endpoint and is_update:
        print_conditional_breaking_change(cli_ctx, tag='CloudUpdateOutputBreakingChange')
    elif arm_endpoint:
        print_conditional_breaking_change(cli_ctx, tag='CloudRegisterOutputBreakingChange')

    _populate_from_metadata_endpoint(c, arm_endpoint)
    required_endpoints = {'resource_manager': '--endpoint-resource-manager',
                          'active_directory': '--endpoint-active-directory',
                          'active_directory_resource_id': '--endpoint-active-directory-resource-id',
                          'active_directory_graph_resource_id': '--endpoint-active-directory-graph-resource-id'}
    missing_endpoints = [e_param for e_name, e_param in required_endpoints.items()
                         if not c.endpoints.has_endpoint_set(e_name)]
    if missing_endpoints and not cloud_is_registered(cli_ctx, cloud_name):
        raise CLIError("The following endpoints are required for the CLI to function and were not specified on the "
                       "command line, in the cloud config or could not be autodetected.\n"
                       "Specify them on the command line or through the cloud config file:\n"
                       "{}".format(', '.join(missing_endpoints)))
    return c


def register_cloud(cmd,
                   cloud_name,
                   cloud_config=None,
                   profile=None,
                   endpoint_management=None,
                   endpoint_resource_manager=None,
                   endpoint_sql_management=None,
                   endpoint_gallery=None,
                   endpoint_active_directory=None,
                   endpoint_active_directory_resource_id=None,
                   endpoint_active_directory_graph_resource_id=None,
                   endpoint_active_directory_data_lake_resource_id=None,
                   endpoint_vm_image_alias_doc=None,
                   suffix_sql_server_hostname=None,
                   suffix_storage_endpoint=None,
                   suffix_keyvault_dns=None,
                   suffix_azure_datalake_store_file_system_endpoint=None,
                   suffix_azure_datalake_analytics_catalog_and_job_endpoint=None,
                   suffix_acr_login_server_endpoint=None):
    c = _build_cloud(cmd.cli_ctx, cloud_name, cloud_config=cloud_config, is_update=False,
                     cloud_args=locals())
    try:
        add_cloud(cmd.cli_ctx, c)
    except CloudAlreadyRegisteredException as e:
        raise CLIError(e)


def modify_cloud(cmd,
                 cloud_name=None,
                 cloud_config=None,
                 profile=None,
                 endpoint_management=None,
                 endpoint_resource_manager=None,
                 endpoint_sql_management=None,
                 endpoint_gallery=None,
                 endpoint_active_directory=None,
                 endpoint_active_directory_resource_id=None,
                 endpoint_active_directory_graph_resource_id=None,
                 endpoint_active_directory_data_lake_resource_id=None,
                 endpoint_vm_image_alias_doc=None,
                 suffix_sql_server_hostname=None,
                 suffix_storage_endpoint=None,
                 suffix_keyvault_dns=None,
                 suffix_azure_datalake_store_file_system_endpoint=None,
                 suffix_azure_datalake_analytics_catalog_and_job_endpoint=None,
                 suffix_acr_login_server_endpoint=None):
    if not cloud_name:
        cloud_name = cmd.cli_ctx.cloud.name
    c = _build_cloud(cmd.cli_ctx, cloud_name, cloud_config=cloud_config, is_update=True,
                     cloud_args=locals())
    try:
        update_cloud(cmd.cli_ctx, c)
    except CloudNotRegisteredException as e:
        raise CLIError(e)


def unregister_cloud(cmd, cloud_name):
    try:
        return remove_cloud(cmd.cli_ctx, cloud_name)
    except CloudNotRegisteredException as e:
        raise CLIError(e)
    except CannotUnregisterCloudException as e:
        raise CLIError(e)


def set_cloud(cmd, cloud_name, profile=None):
    try:
        cloud_name = _get_cloud_name(cmd.cli_ctx, cloud_name)
        switch_active_cloud(cmd.cli_ctx, cloud_name)
        if profile:
            modify_cloud(cmd, cloud_name=cloud_name, profile=profile)
    except CloudNotRegisteredException as e:
        raise CLIError(e)


def list_profiles(cmd, cloud_name=None, show_all=False):
    from azure.cli.core.profiles import API_PROFILES
    if not cloud_name:
        cloud_name = get_active_cloud_name(cmd.cli_ctx.cloud)
    return list(API_PROFILES)
