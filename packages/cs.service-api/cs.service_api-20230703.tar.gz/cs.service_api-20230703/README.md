ServiceAPI, a base class for APIs which talk to a service,
typically a web service via HTTP.

*Latest release 20230703*:
Retry logic for requests.

An instance of a `ServiceAPI` embodies some basic features
that feel common to web based services:
- a notion of a login
- local state, an `SQLTags` for data about entities of the service
- downloads, if that is a thing, with `FSTags` for file annotations

## Class `HTTPServiceAPI(ServiceAPI, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin)`

`HTTPServiceAPI` base class for other APIs talking to HTTP services.

Subclasses must define:
* `API_BASE`: the base URL of API calls.
  For example, the `PlayOnAPI` defines this as `f'https://{API_HOSTNAME}/v3/'`.

*Method `HTTPServiceAPI.json(self, suburl, _response_encoding=None, **kw)`*:
Request `suburl` from the service, by default using a `GET`.
Return the result decoded as JSON.

Parameters are as for `HTTPServiceAPI.suburl`.

## Class `RequestsNoAuth(requests.auth.AuthBase)`

This is a special purpose subclass of `requests.auth.AuthBase`
to apply no authorisation at all.
This is for services with their own special purpose authorisation
and avoids things like automatic netrc based auth.

## Class `ServiceAPI(cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin)`

`SewrviceAPI` base class for other APIs talking to services.

*Method `ServiceAPI.available(self) -> Set[cs.sqltags.SQLTagSet]`*:
Return a set of the `SQLTagSet` instances representing available
items at the service, for example purchased books
available to your login.

*Method `ServiceAPI.get_login_state(self, do_refresh=False) -> cs.sqltags.SQLTagSet`*:
The login state, a mapping. Performs a login if necessary
or if `do_refresh` is true (default `False`).

*Method `ServiceAPI.login(self) -> Mapping`*:
Do a login: authenticate to the service, return a mapping of related information.

Not all services require this and we expect such subclasses
to avoid use of login-based methods.

*Property `ServiceAPI.login_expiry`*:
Expiry UNIX time for the login state.
This implementation returns `None`.

*Property `ServiceAPI.login_state`*:
The login state, a mapping. Performs a login if necessary.

*Method `ServiceAPI.startup_shutdown(self)`*:
Start up: open and init the `SQLTags`, open the `FSTags`.

# Release Log



*Release 20230703*:
Retry logic for requests.

*Release 20230217*:
Initial release.
