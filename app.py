from constructs import Construct
from aws_cdk import (
    App, Stack,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_lambda as lambda_
)

class HelloWorldLambdaStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, "HelloWorldBucketTest")

        handler = lambda_.Function(self, "HelloWorldLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("resources"),
            handler="helloWorld.lambda_handler",
            environment=dict(
            BUCKET=bucket.bucket_name)
        )

        bucket.grant_read_write(handler)

        api = apigateway.RestApi(self, "hello-world-api",
                  rest_api_name="Hello World API",
                  description="Test services for developing test")

        get_hello_world_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_hello_world_integration)   # GET /

app = App()
HelloWorldLambdaStack(app, "HelloWorldLambdaStack")
app.synth()