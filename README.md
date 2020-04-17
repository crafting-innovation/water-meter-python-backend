# Steps:

1. Create a S3 bucket in the same region where you want to run the script.
Let's say you named the bucket: demo-cfn-infra-resources

2. Run the Following commands one by one

aws cloudformation package \
--template-file cloudformation-template.sam.yaml \
--s3-bucket demo-cfn-infra-resources \
--output-template-file .cloudformation-template.yaml

aws cloudformation deploy \
--template-file .cloudformation-template.yaml \
--capabilities CAPABILITY_NAMED_IAM \
--stack-name gourav-bootstrap-stack-dev \
--parameter-overrides  \
Environment=dev ServiceName=gourav-bootstrap-stack DynamoDBTableName=dev-gourav-dynamo-table

3. Go to AWS Cloudformation in your region to see the progress.

4. Once it is complete, you will see the following AWS resources created:
- ApiGatewayInvokeLambdaPermission
- ApiIAMRole
- CognitoIdentityAuthRole
- CognitoIdentityAuthRole
- CognitoIdentityPoolRoles
- CognitoUserPool
- CognitoUserPoolClient	
- DeadLetterQueue
- DynamoTable
- LambdaFunction
- LambdaFunctionDaily
- LambdaFunctionDailyPermission
- LambdaIAMRole
- AWSApiGateway
- AWSApiGatewayDeployment
- AWSApiGatewayStage

5. Cleanup the generated template by running the following command
rm .cloudformation-template.yaml

6. Everything is already created and connected to each other. So only thing you would need to do 
is: 
- Add business logic to Python Lambda function.
- Add various API endpoints to API gateway.
- Change naming as required.
- Add additional dynamo table if required.

7. Make sure if you need any update, then update the original cloudformation file and run the commands from 
step 2 to step 5 again.