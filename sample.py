from google.auth.transport import mtls
import google.oauth2.credentials
from google.pubsub import PublisherClient
import google.api_core.client_options as ClientOptions


# Fill in your project_id.
project_id = <your_project_id>


def list_topics():
    # Get the user access token.
    cred = google.oauth2.credentials.UserAccessTokenCredentials()

    # If device client certificate exists, it will be used to establish mutual TLS connection,
    # and the pubsub client will automatically switch to pubsub mtls endpoint.
    # If device client certificate doesn't exists, mutual TLS connection will not be established,
    # and the default mtls endpoint will be used.
    # The existence of device client certificate can be checked via 
    # 'mtls.has_default_client_cert_source()'. You can call 'mtls.default_client_cert_source()'
    # to get a callback, which produces the client certificate on execution. 
    if mtls.has_default_client_cert_source():
        print("Default client cert source is found. It will be used to create mutual TLS channel")
        callback = mtls.default_client_cert_source()
    else:
        print("Default client cert source is not found. Mutual TLS channel will not be created")
        callback = None

    # Pass the callback to ClientOptions, and pass the ClientOptions to PublisherClient. 
    client_options = ClientOptions.ClientOptions(
        client_cert_source=callback
    )
    client = PublisherClient(credentials=cred, client_options=client_options)

    # Call the pubsub list_topics api.
    project = "projects/{}".format(project_id)
    list_topics_iter = client.list_topics(project=project)

    # Print out the result.
    topics = list(list_topics_iter)
    print(topics)


list_topics()
