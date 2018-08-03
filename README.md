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

To test, run
```
python -m unittest -v test.py
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
