# skype-contact-parser

Get any Skype contact by phone number! And do Skype search by any term, literally.

This script exploits Skype search functionality.

## Usage

You need to authorize first to get Skype token. You can:

1. Use env variables
```sh
export SKYPE_LOGIN=login
export SKYPE_PASS=pass
```

2. Enter credentials after the launch:
```
./search.py +79218657070
Login: 
Password: 
```
Script will get the token and save it to the `token.txt` file.

## Development

Set `SKPY_DEBUG_HTTP=1` in your environment to output all HTTP requests between the library and Skype’s APIs.

Read the unoffical `skpy` library documentation [here](https://skpy.t.allofti.me/).