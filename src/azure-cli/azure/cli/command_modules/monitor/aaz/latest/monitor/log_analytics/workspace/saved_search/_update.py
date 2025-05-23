# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


class Update(AAZCommand):
    """Update a saved search for a given workspace.

    :example: Update a saved search for a given workspace.
        az monitor log-analytics workspace saved-search update -g MyRG --workspace-name MyWS -n MySavedSearch --category Test1 --display-name TestSavedSearch -q "AzureActivity | summarize count() by bin(TimeGenerated, 1h)" --fa myfun --fp "a:string = value"
    """

    _aaz_info = {
        "version": "2020-08-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.operationalinsights/workspaces/{}/savedsearches/{}", "2020-08-01"],
        ]
    }

    AZ_SUPPORT_GENERIC_UPDATE = True

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.saved_search_name = AAZStrArg(
            options=["-n", "--name", "--saved-search-name"],
            help="Name of the saved search and it's unique in a given workspace.",
            required=True,
            id_part="child_name_1",
        )
        _args_schema.workspace_name = AAZStrArg(
            options=["--workspace-name"],
            help="The name of the workspace.",
            required=True,
            id_part="name",
            fmt=AAZStrArgFormat(
                pattern="^[A-Za-z0-9][A-Za-z0-9-]+[A-Za-z0-9]$",
                max_length=63,
                min_length=4,
            ),
        )

        # define Arg Group "Parameters"

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.category = AAZStrArg(
            options=["--category"],
            arg_group="Properties",
            help="The category of the saved search. This helps the user to find a saved search faster. ",
        )
        _args_schema.display_name = AAZStrArg(
            options=["--display-name"],
            arg_group="Properties",
            help="Saved search display name.",
        )
        _args_schema.func_alias = AAZStrArg(
            options=["--fa", "--func-alias"],
            arg_group="Properties",
            help="Function Aliases are short names given to Saved Searches so they can be easily referenced in query. They are required for Computer Groups.",
            nullable=True,
        )
        _args_schema.func_param = AAZStrArg(
            options=["--fp", "--func-param"],
            arg_group="Properties",
            help="The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://learn.microsoft.com/azure/kusto/query/functions/user-defined-functions.",
            nullable=True,
        )
        _args_schema.saved_query = AAZStrArg(
            options=["-q", "--saved-query"],
            arg_group="Properties",
            help="The query expression for the saved search.",
        )
        _args_schema.tags = AAZListArg(
            options=["--tags"],
            arg_group="Properties",
            help="The tags attached to the saved search.",
            nullable=True,
        )
        _args_schema.version = AAZIntArg(
            options=["--version"],
            arg_group="Properties",
            help="The version number of the query language. The current version is 2 and is the default.",
            nullable=True,
        )

        tags = cls._args_schema.tags
        tags.Element = AAZObjectArg(
            nullable=True,
        )

        _element = cls._args_schema.tags.Element
        _element.name = AAZStrArg(
            options=["name"],
            help="The tag name.",
        )
        _element.value = AAZStrArg(
            options=["value"],
            help="The tag value.",
        )
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.SavedSearchesGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        self.SavedSearchesCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    # @register_callback
    def pre_operations(self):
        pass

    # @register_callback
    def post_operations(self):
        pass

    # @register_callback
    def pre_instance_update(self, instance):
        pass

    # @register_callback
    def post_instance_update(self, instance):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class SavedSearchesGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/savedSearches/{savedSearchId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "savedSearchId", self.ctx.args.saved_search_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.workspace_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2020-08-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _build_schema_saved_search_read(cls._schema_on_200)

            return cls._schema_on_200

    class SavedSearchesCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/savedSearches/{savedSearchId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "MgmtErrorFormat"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "savedSearchId", self.ctx.args.saved_search_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "workspaceName", self.ctx.args.workspace_name,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2020-08-01",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=self.ctx.vars.instance,
            )

            return self.serialize_content(_content_value)

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _build_schema_saved_search_read(cls._schema_on_200)

            return cls._schema_on_200

    class InstanceUpdateByJson(AAZJsonInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance(self.ctx.vars.instance)

        def _update_instance(self, instance):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=instance,
                typ=AAZObjectType
            )
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("category", AAZStrType, ".category", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("displayName", AAZStrType, ".display_name", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("functionAlias", AAZStrType, ".func_alias")
                properties.set_prop("functionParameters", AAZStrType, ".func_param")
                properties.set_prop("query", AAZStrType, ".saved_query", typ_kwargs={"flags": {"required": True}})
                properties.set_prop("tags", AAZListType, ".tags")
                properties.set_prop("version", AAZIntType, ".version")

            tags = _builder.get(".properties.tags")
            if tags is not None:
                tags.set_elements(AAZObjectType, ".")

            _elements = _builder.get(".properties.tags[]")
            if _elements is not None:
                _elements.set_prop("name", AAZStrType, ".name", typ_kwargs={"flags": {"required": True}})
                _elements.set_prop("value", AAZStrType, ".value", typ_kwargs={"flags": {"required": True}})

            return _instance_value

    class InstanceUpdateByGeneric(AAZGenericInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance_by_generic(
                self.ctx.vars.instance,
                self.ctx.generic_update_args
            )


_schema_saved_search_read = None


def _build_schema_saved_search_read(_schema):
    global _schema_saved_search_read
    if _schema_saved_search_read is not None:
        _schema.etag = _schema_saved_search_read.etag
        _schema.id = _schema_saved_search_read.id
        _schema.name = _schema_saved_search_read.name
        _schema.properties = _schema_saved_search_read.properties
        _schema.type = _schema_saved_search_read.type
        return

    _schema_saved_search_read = AAZObjectType()

    saved_search_read = _schema_saved_search_read
    saved_search_read.etag = AAZStrType()
    saved_search_read.id = AAZStrType(
        flags={"read_only": True},
    )
    saved_search_read.name = AAZStrType(
        flags={"read_only": True},
    )
    saved_search_read.properties = AAZObjectType(
        flags={"required": True, "client_flatten": True},
    )
    saved_search_read.type = AAZStrType(
        flags={"read_only": True},
    )

    properties = _schema_saved_search_read.properties
    properties.category = AAZStrType(
        flags={"required": True},
    )
    properties.display_name = AAZStrType(
        serialized_name="displayName",
        flags={"required": True},
    )
    properties.function_alias = AAZStrType(
        serialized_name="functionAlias",
    )
    properties.function_parameters = AAZStrType(
        serialized_name="functionParameters",
    )
    properties.query = AAZStrType(
        flags={"required": True},
    )
    properties.tags = AAZListType()
    properties.version = AAZIntType()

    tags = _schema_saved_search_read.properties.tags
    tags.Element = AAZObjectType()

    _element = _schema_saved_search_read.properties.tags.Element
    _element.name = AAZStrType(
        flags={"required": True},
    )
    _element.value = AAZStrType(
        flags={"required": True},
    )

    _schema.etag = _schema_saved_search_read.etag
    _schema.id = _schema_saved_search_read.id
    _schema.name = _schema_saved_search_read.name
    _schema.properties = _schema_saved_search_read.properties
    _schema.type = _schema_saved_search_read.type


__all__ = ["Update"]
