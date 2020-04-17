# python-gapic-pubsub-mtls-sample
A sample showing how to generate pubsub client using gapic-generator-python, and how to use device certificate to estalish mutual TLS connection.

# How to run the sample.

## 1. Log in with gcloud.

```
$ gcloud auth login
$ gcloud config set project <your_project_id>
```
Your project should have pubsub api enabled, and VPC policy set to enforce client certificate checking.

## 2. Download the repo and fill in your project id.

```
$ git clone https://https://github.com/arithmetic1728/python-gapic-pubsub-mtls-sample.git
$ cd python-gapic-pubsub-mtls-sample
```

Now open `sample.py` and fill in your project id.

## 3. Create a python virtual environment and install the dependencies.

```
$ pyenv virtualenv mtls-sample
$ pyenv local mtls-sample
$ python -m pip install -e pubsub/
```

## 4. Run the sample.

```
$ python sample.py
```

You should see the list of topics if everything is set up correctly. You may see `403` permission denied error if there are any problems with the client certificate or user access token.
