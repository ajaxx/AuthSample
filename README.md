# Overview

This project was originally created as a reference implementation against the oauth.com flows.  It's
purpose was to demonstrate how you could build a client service which leveraged a resource in another
service (service provider) using the OAuth 2 protocol.

That same vision persists to this day, but I have since modified the sample to account for some hurdles
that we had to overcome.  As nice as the oauth.com reference samples are, some of the mechanics just
don't seem to work.

# Implementation

The application written herein is based on flask (a web framework for python).  It is based 
on [RFC 6749](https://www.rfc-editor.org/rfc/rfc6749).  Most of this implementation is based
on the authorization grant flow which is outlined in section 4.

# Configuration

In order to use this application you must configure the service_provider.json file.  It
contains the endpoints for authorization and token exchange.  It also includes the scope
and your client-id and client secret.

## Configuring with Okta

If you have a developer account with Okta, then you can setup your application and just
plug in a few key configurables.  Be sure to grant your application scopes or you will
find yourself getting denied.

```
{
    "client_id" : "1234567",
    "client_secret" : "MjM5MjA2NzktZmI3OS00NmU1LWI5ZmYtZTllZTAwZGJlM2Nj",
    "authorization_endpoint": "https://dev-21212.okta.com/oauth2/v1/authorize",
    "token_endpoint": "https://dev-21212.okta.com/oauth2/v1/token",
    "scope" : "okta.users.read.self"
}
```

# Running

Running the application is pretty simple:

`python app.py`

This will start the application which will bind to localhost:5000.  Point your browser
at http://localhost:5000/.  This will popup a screen with a basic message and asking you
to authorize.  What happens next??? Well, that depends on your service provider, but I
tested this against Okta.

If all goes well, you'll be asked to login to your service provider and then redirected
back to the application with an auth token.  The client will take the auth token and
exchange it for an access token.  The client will then show you the access token and
other details.