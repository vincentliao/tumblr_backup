# tumblr backup manager

## prerequisite 

* Tumblr API client: [pytumblr](https://github.com/tumblr/pytumblr)
* [Register an App in Tumblr](https://www.tumblr.com/docs/en/api/v2#auth)

## how to use

* Make a copy of `account.py.sample` and rename it as `account.py`
* Get 4 authentication infomation below in Tumplr:
	- consumer_key
	- consumer_secret
	- oauth_secret
	- oauth_token
* Execute with commnad. backup files will store in local folder named `backup`.

	```
	$ python tumblr_backup.py
	```

