-- Table: public.reset_password_token

-- DROP TABLE IF EXISTS public.reset_password_token;

CREATE TABLE IF NOT EXISTS public.reset_password_token
(
    id integer NOT NULL DEFAULT nextval('reset_password_token_id_seq'::regclass),
    user_id integer,
    token character varying COLLATE pg_catalog."default",
    date_created timestamp without time zone,
    CONSTRAINT reset_password_token_pkey PRIMARY KEY (id),
    CONSTRAINT reset_password_token_user_id_key UNIQUE (user_id),
    CONSTRAINT reset_password_token_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.reset_password_token
    OWNER to admin;
-- Index: ix_reset_password_token_id

-- DROP INDEX IF EXISTS public.ix_reset_password_token_id;

CREATE INDEX IF NOT EXISTS ix_reset_password_token_id
    ON public.reset_password_token USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_reset_password_token_token

-- DROP INDEX IF EXISTS public.ix_reset_password_token_token;

CREATE INDEX IF NOT EXISTS ix_reset_password_token_token
    ON public.reset_password_token USING btree
    (token COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
