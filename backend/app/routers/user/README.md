# User Router

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

users of AfriLegal API.


## Files

* [models.py](./models.py): Contains classes with
	                    database tables for
	                    ORM integration.
	                    Classes include:

	* `User`-> instances:
		* id
		* email
		* password
		* status
		* user_type_id

	* `UserInfo`-> instances:
		* id
		* user_id
		* first_name
		* middle_name
		* last_name

	* `ResetPasswordToken` -> instances:
		* id
		* user_id
		* token
		* date_created


* [schemas.py](./schemas.py): Contains classes
			      that define schemas
			      for entering into
			      database tables.
			      Classes include:

	* `UserBase` -> instances:
		* `email`: EmailStr

	* `UserCreate` -> instances:
		* `password`: str
		* `user_type_id`: int
		* `status`: bool

	* `UserUpdate` -> instances:
		* `first_name`: str
		* `middle_name`: str
		* `last_name`: str

	* `ResetPassword` -> instances:
                * `password`: str
		* `code`: str

	* `ChangePassword` -> instances:
                * `email`: str
		* `password`: str

	* `User` -> instances:
		* `id`: int
		* `user_type_id`: str


* [crud.py](./crud.py): Contains functions that
			creates, reads, updates
			and deletes users.
			They include:
	* is_token_blacklisted
	* read_users
	* read_users_auth
	* read_user_by_id
	* read_user_by_id_auth
	* read_user_by_email
	* read_user_by_email_auth
	* create_user
	* create_user_auth
	* verify_password
	* verify_password_auth
	* read_hash_code
	* read_hash_table
	* reset_password
	* reset_password_auth
	* reset_password`_`
	* reset_password_auth`_`
	* change_password
	* verify_code
	* verify_code_auth
	* verify_code`_`
	* verify_code_auth`_`
	* update_user
	* update_user_auth
	* delete_user
	* delete_user_auth


* [main.py](./main.py): Contains functions that
			defines enpoints to call
			**CRUD** functions. They
			include:

	* `read_all_users`
	* `read_a_user_by_id`
	* `read_user_by_email`
	* `verify_hash_details`
	* `read_hash_table`
	* `create_user`
	* `verify_password`
	* `update_user`
	* `update_password`
	* `update_password_`
	* `change_password`
	* `delete_user`


## Endpoints

* **GET**: `/get_users`
* **GET**: `/get/{id}`
* **GET**: `/{email}/`
* **GET**: `/verify_hash`
* **GET**: `/read_hash_tabl`
* **POST**: `/create_user`
* **POST**: `/verify/password`
* **PATCH**: `/update/{id}`
* **PATCH**: `/{id}/password`
* **PATCH**: `/password`
* **PUT**: `/change/password`
* **DELETE**: `/delete/{id}`

