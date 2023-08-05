# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lambda_handler', 'lambda_handler.model']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'lambda-handler',
    'version': '1.1.1',
    'description': 'A Python package for routing and validating AWS events inside a Lambda function',
    'long_description': '# Lambda Handler\n\nThis project defines a Python class, `LambdaHandler`, and associated Pydantic-derived\nevent classes, for handling API Gateway events from a range of sources, in particular:\n\n- Direct Invocation\n- EventBridge\n- SQS queues\n- SNS topics\n\nWhen not using the optional FastAPI support (see below), the package\'s only dependency\nis pydantic.\n\n## Use\n\n```python\nfrom lambda_handler import (\n    LambdaHandler,\n    EventBridgeEvent,\n    SnsEvent,\n    LambdaResponse,\n)\n\nhandler = LambdaHandler()\n\n@handler.sns(topic_name="MyTopic")\ndef handle_mytopic(event: SnsEvent) -> LambdaResponse:\n    body = frobincate()\n    return LambdaResponse(status_code=200, body=body)\n\n@handler.event_bridge(resource_name="MyResource")\ndef handle_myresource(event: EventBridgeEvent) -> LambdaResponse:\n    body = fizzbuzz()\n    return LambdaResponse(status_code=200, body=body)\n```\n\nThe handler looks after both the event parsing (so your functions should always\naccept an event of some `*Event` type), and its response as a properly-formatted\ndictionary.\n\n## Combining with FastAPI\n\nA notable omission from the events that are handled by `LambdaHandler` directly are\nHTTP requests. These can be handled by an instance of `FastAPI`, as follows:\n\n```python\nfrom fastapi import FastAPI\nfrom lambda_handler import LambdaHandler\n\napp = FastAPI(title="My HTTP handler")\n\n@app.get("/")\ndef index():\n    return "Hello, World!"\n\nhandler = LambdaHandler(fastapi_app=app)\n```\n\nThe handler will then take care of everything on your behalf. If you\'d prefer, you\ncan set `fastapi_app` later instead, and the handler will take care of that, too.\n\n```python\nfrom fastapi import FastAPI\nfrom lambda_handler import LambdaHandler, SnsEvent, LambdaResponse\n\nhandler = LambdaHandler()\n\n@handler.sns(topic_name="MyTopic")\ndef handle_mytopic(event: SnsEvent) -> LambdaResponse:\n    body = frobincate()\n    return LambdaResponse(status_code=200, body=body)\n\n\napp = FastAPI(title="My HTTP handler")\n\n@app.get("/")\ndef index():\n    return "Hello, World!"\n\nhandler.fastapi_app = app\n```\n\nFastAPI support requires the package to be installed with optional extras:\n`pip install "lambda-handler[fastapi]"`, and is built on top of the existing\n[Mangum](https://mangum.io/) package.\n\n## Model Validation\n\nThe `*Event` models lambda-handler defines use [pydantic](pydantic-docs.helpmanual.io/)\nfor parsing and validation, and these models are _generic_. This means that you can\npass a type argument to the class when defining your function, and it will correctly\nparse the content of the event (see below) to that type. If this is confusing, it\'s\neasier to see it in action:\n\n```python\nfrom lambda_handler import LambdaHandler, SnsEvent, LambdaResponse\nfrom pydantic import BaseModel\n\nhandler = LambdaHandler()\n\nclass MyModel(BaseModel):\n    thing: str\n\n@handler.sns(topic_name=topic_name)\ndef test_func(event: SnsEvent[MyModel]) -> LambdaResponse:\n    assert isinstance(event.records[0].sns.message, MyModel)\n    return LambdaResponse(status_code="200")\n```\n\nHere, we have parametrised `SnsEvent` with `MyModel` in the signature of `test_func`,\nmeaning that the `message` attribute is parsed to a `MyModel` instance in the process.\n\n### Parametrised Event Attributes\n\nThe following attributes are those which are parsed to a Pydantic model for each event\ntype:\n\n| Event Type              | Parsed Attribute                  |\n|:------------------------|:----------------------------------|\n| `DirectInvocationEvent` | `event.direct_invocation.body`    |\n| `EventBridgeEvent`      | `event.detail`                    |\n| `SnsEvent`              | `event.records[i].sns.message`    |\n| `SqsEvent`              | `event.records[i].body`           |\n\n\n## Dealing with Raw Data\n\nIf you don\'t want to deal with parsed event objects, you can include the `raw=True`\nparameter to any of the wrapping methods of `LambdaHandler` and write a function\nthat accepts and returns a `Dict[str, Any]` instead. Note that, in this case, the\nevent object will still be parsed by the `AwsEvent` subclasses for identification,\nbut the event object will be passed as-is in dictionary format to the function.\n\n```python\nfrom fastapi import FastAPI\nfrom lambda_handler import LambdaHandler, SnsEvent, LambdaResponse\n\nfrom typing import Any, Dict\n\nhandler = LambdaHandler()\n\n@handler.sns(topic_name="MyTopic")\ndef handle_mytopic(event: SnsEvent) -> LambdaResponse:\n    body = frobincate()\n    return LambdaResponse(status_code=200, body=body)\n\n@handler.sns(topic_name="MyOtherTopic". raw=True)\ndef handle_mytopic(event: Dict[str, Any]) -> Dict[str, Any]:\n    body = frobincate()\n    return {"statusCode": "200"}\n```\n',
    'author': 'Matthew Badger',
    'author_email': 'matt@branchenergy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/branchenergy/lambda_handler',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
