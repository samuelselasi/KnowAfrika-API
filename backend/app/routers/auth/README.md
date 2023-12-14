# Authentication Router

## Content

* [About](#about)
* [Files](#files)
* [Endpoints](#endpoints)


## About

This router contains files for handling
endpoints that:

* Reads -> `GET`,
* Creates -> `POST`,
* Updates -> `PUT` or `PATCH` and
* Deletes -> `DELETE`

authentication of the endpoints
in this application.


## Files

* [models.py](./models.py): Contains classes with
	                    database tables for
	                    ORM integration.
	                    Classes include:

	* `ResetPasswordCodes`-> instances:
		* id
		* code
		* user_id
		* user_email
		* status
		* date_created
		* date_modified

	* `RevokedToken`-> instances:
		* id
		* jti
		* date_created
		* date_modified

* [schemas.py](./schemas.py): Contains classes
			      that define schemas
			      for entering into
			      database tables.
			      Classes include:

	* `Auth` -> instances:
		* `password`: str

	* `AuthResponse` -> instances:
		* `access_token`: str
		* `refresh_token: str
		* `user`: User

	* `Token` -> instances:
		* `access_token`: str
		* `refresh_token`: str

* [crud.py](./crud.py): Contains functions that
			creates, reads, updates
			and deletes tokens.
			They include:
	* authenticate
	* revoke_token
	* refresh_token
	* is_token_blacklisted
	* request_password_reset
	* request_password_reset`_`
	* get_current_user
	* delete_password_reset_code

* [main.py](./main.py): Contains functions that
			defines enpoints to call
			**CRUD** functions. They
			include:

	* `get_current_user`
	* `authenticate`
	* `logout`
	* `refresh_token`
	* `request_password_reset`


## Endpoints

* **GET**: `/current_user`
* **POST**: `/login`
* **POST**: `/logout`
* **POST**: `/refresh`
* **POST**: `/request`

