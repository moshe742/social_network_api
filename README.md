# social_network_api

This is a test for a company that I received and this is the result.
I assume all the mails I have are valid, so I check only for undeliverable
on hunter api.

## how to use the api?

On the API one have four endpoints, all start with api/ and then the relevant
word, one can signup, login, post and like (or unlike) a post, all done with
REST API.

To make everything work one must create a few environment varivables with their
relevant info:

* HUNTER_SECRET_KEY
* SOCIAL_SECRET
* CLEARBIT_SECRET_KEY

Without those it won't work, so create them as needed.
HUNTER_SECRET_KEY is the secret key one have from hunber api.
SOCIAL_SECRET should be a random string for the secret_key of Django.
CLEARBIT_SECRET_KEY is the secret key one have from clrearbit api.

The urls are:
* api/signup/
* api/login/
* api/posts/
* api/posts/<post-id>/

On signup one sign to the api, and should send a json with those keys:

* username
* password
* email

If all is well one will get the username, email and user_id back in the
response.

On login one login to the system, and should send a json with those keys:

* username
* password

On successfull login one will get a token to be sent on every request in the
Authorization header.

On posts one should send a json with this key:

* content

And with Authorization header having the token received on login on the key token.

on like one should use as above the Authorization header and send a json that
includes the keys:

* like

Which must have one of "like" or "unlike"

### bot

There is a bot that can signup emails with running number and get data on them
from hunter and clearbit, then create posts on their behalf, then likes the
posts randomly.

Every kind of request is done on another function according to the requirements.
