INSERT INTO public.users (name, surname, login, password, user_role, ip_address) 
VALUES ('Admin', '', 'Admin', '72d52f053c9c50f8f7d9a25c776c299e71b32b997fd3cf7f7cf20b0e92a0e042', 1, NULL) 
ON CONFLICT (login) DO UPDATE SET
	name =  'Admin',
	password = '72d52f053c9c50f8f7d9a25c776c299e71b32b997fd3cf7f7cf20b0e92a0e042',
	user_role = 1,
	deleted_at = NULL;