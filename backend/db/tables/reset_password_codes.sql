-- Table: public.reset_password_codes

-- DROP TABLE IF EXISTS public.reset_password_codes;

CREATE TABLE IF NOT EXISTS public.reset_password_codes
(
    id integer NOT NULL DEFAULT nextval('reset_password_codes_id_seq'::regclass),
    code character varying COLLATE pg_catalog."default",
    user_id integer,
    user_email character varying COLLATE pg_catalog."default",
    status boolean NOT NULL,
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    CONSTRAINT reset_password_codes_pkey PRIMARY KEY (id),
    CONSTRAINT reset_password_codes_code_key UNIQUE (code),
    CONSTRAINT reset_password_codes_user_email_key UNIQUE (user_email),
    CONSTRAINT reset_password_codes_user_id_key UNIQUE (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.reset_password_codes
    OWNER to admin;
-- Index: ix_reset_password_codes_id

-- DROP INDEX IF EXISTS public.ix_reset_password_codes_id;

CREATE INDEX IF NOT EXISTS ix_reset_password_codes_id
    ON public.reset_password_codes USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
