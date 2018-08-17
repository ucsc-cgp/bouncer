[![Build Status](https://travis-ci.org/ucsc-cgp/bouncer.svg?branch=master)](https://travis-ci.org/ucsc-cgp/bouncer)

# bouncer
Simple email whitelist checker backed by the AWS Secrets Manager

## setup

### regular
Either add `cgp-bouncer` to your project requirements or
```
pip install cgp-bouncer
```
in a Python 3 virtualenv.

### for development
Instead of the steps above clone the repo, `cd` into the repo, and run
```
pip install -e .
```
and
```
pip install -r requirements-dev.txt
```

To test, run
```
tox
```
## how to use

### setting up the whitelist
1. Go to the AWS Console and find the **Secrets Manager** service.
1. Select **Store a new secret**.
1. For secret type select **Other type of secrets**.
1. Under the **Secret key/value** tab enter `email` as the key and a
   comma separated (no spaces) list of whitelisted emails as the
   value. Select **Next**.
1. Name your secret something descriptive, such as 
   `commons/dev/whitelist` and give it a description. Select **Next**.
1. Make sure **Disable automatic rotation** is selected. Then select
   **Next**.
1. Review your configuration and select **Store**.

### adding someone to the whitelist
1. Go to the AWS Console and find the **Secrets Manager** service.
1. Find the secret to which you want to add. For example, one might
   search for `commons/dev/whitelist`.
1. Under **Secret value**, select **Retrieve secret value**. Then
   select **Edit**. 
1. Add your email with **NO WHITESPACE** to the comma separated list
   under the key `email` and select **Save**.
   
### allowing access to the whitelist
Programs which use the whitelist, such as the Commons HCA DSS, must be given
access to the email whitelist secret in Secrets Manager using AWS IAM policy configuration.
To add an IAM policy for a specific secret, perform the following steps 
(which currently can only be performed through the AWS CLI, not the AWS Console UI):
1. Ensure that recent version of `awscli` is installed:
    ```
    pip install --upgrade awscli
    ```
2. Create a file containing the desired policy to control the secret.
    For example, to allow a DSS API lambda to get a secret value:
    * DSS API Lambda Role ARN: `arn:aws:iam::719818754276:role/dss-commonsdev`
    * Secret Name: `commons/dev/whitelist`
    * Secret ARN: `arn:aws:secretsmanager:us-west-2:719818754276:secret:commons/dev/whitelist-QoQLrQ`
    
    create a policy like the following:
    ```
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "arn:aws:iam::719818754276:role/dss-commonsdev" },
                "Action": "secretsmanager:GetSecretValue",
                "Resource": "arn:aws:secretsmanager:us-west-2:719818754276:secret:commons/dev/whitelist-QoQLrQ"
            }
        ]
    }
    ```
    
    Note: This type of policy configuration can also be used to control which users can access or modify the secret.

3. Run: 
    ```
    aws secretsmanager put-resource-policy --secret-id commons/dev/whitelist --resource-policy file://secretpolicy.json
    ```
    which should produce output like the following:
    ```
    {
        "ARN": "arn:aws:secretsmanager:us-west-2:719818754276:secret:commons/dev/whitelist-QoQLrQ",
        "Name": "commons/dev/whitelist"
    }
    ```

For more information, see the following AWS documentation:
* [Overview of Managing Access Permissions to Your Secrets Manager Secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_overview.html)
* [Using Identity-based Policies (IAM Policies) for Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_identity-based-policies.html)
* [Using Resource-based Policies for Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_resource-based-policies.html)
* [Actions, Resources, and Context Keys You Can Use in an IAM Policy or Secret Policy for AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_iam-permissions.html)
* [Managing a Resource-based Policy for a Secret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_secret-policy.html)
    * This reference is the most specific, and likely to be the most helpful.

#### troubleshooting whitelist access issues
With respect to the example described above, incorrect or missing policy configuration for a secret will typically result in both of the following:
* An HTTP code `500 Internal server error` being reported by the client
* A detailed error message written to the Lambda log describing the problem in detail. For example:
    ```
    ...
    botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the GetSecretValue operation: User: arn:aws:sts::719818754276:assumed-role/dss-commonsdev/dss-commonsdev is not authorized to perform: secretsmanager:GetSecretValue on resource: arn:aws:secretsmanager:us-west-2:719818754276:secret:commons/commonsdev/whitelist-wZ3Tkl
    ```
This may be resolved by identifying and correcting the policy configuration error.

### using bouncer to check the whitelist
Using is simple!

Here's an example

```python
>>> from bouncer import Bouncer
>>> b = Bouncer('commons/dev/whitelist')
>>> b.is_authorized('valid.email@example.com')
True
>>> b.is_authorized('evil.gnomes@example.com')
False
```

This checks the AWS Secret Keeper called `commons/dev/whitelist` to see
if the users `valid.email@example.com` and `evil.gnomes@example.com`
are in the whitelist.
