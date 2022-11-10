# skype-contact-parser

Get any Skype contact by phone number! And do Skype search by any term, literally.

How it works? This script exploits Skype search API functionality.

WARNING: Skype antifraud system bans accounts periodically. You should check your mailbox
and reset passwords through Microsoft email link when you account stop working. Also, you can
create several accounts and use 3rd option of authorization (see below).

## Usage

**The tool based on the template [osint-cli-tool-skeleton](https://github.com/soxoj/osint-cli-tool-skeleton)**. Read its README to explore all the available functionality.

You need to authorize first to get Skype token. You can:

1. Use env variables
```sh
export SKYPE_LOGIN=login
export SKYPE_PASS=pass
```

2. Enter credentials after the launch:
```
./run.py +79218657070
Login: 
Password: 
```

3. Use special file `credentials.txt` with `login:password` pairs, the tool will automatically select the working one.
```
login1:pass1
login2:pass2
```

Script will get the token and save it to the `token.txt` file.

## Development

Set `SKPY_DEBUG_HTTP=1` in your environment to output all HTTP requests between the library and Skype’s APIs.

Read the unoffical `skpy` library documentation [here](https://skpy.t.allofti.me/).
