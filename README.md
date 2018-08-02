# bouncer
The whitelist checker for authentication with CGP HCA Data Store

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
Using is simple!

Here's an example

```python
>>> from bouncer import Bouncer
>>> b = Bouncer('commons/dev/whitelist')
>>> b.is_authorized('jrbrenna@ucsc.edu')
True
>>> b.is_authorized('evil.gnomes@ucsc.edu')
False
```

This checks the AWS Secret Keeper called `commons/dev/whitelist` to see
if the users `jrbrenna@ucsc.edu` and `evil.gnomes@ucsc.edu` are in the
whitelist.

## adding users to the whitelist
1. Go to the AWS Console and find the **AWS Secrets Manager** service.
1. Find the secret to which you want to add. For example, one might
   search for `commons/dev/whitelist`.
1. Under **Secret value** select **Edit**.
1. Add your email with **NO WHITESPACE** to the comma separated list
   under the key `email`.
