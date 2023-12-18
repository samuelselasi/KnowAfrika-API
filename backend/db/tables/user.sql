-- Table: public.user

-- DROP TABLE IF EXISTS public."user";

CREATE TABLE IF NOT EXISTS public."user"
(
    id integer NOT NULL DEFAULT nextval('user_id_seq'::regclass),
    email character varying COLLATE pg_catalog."default",
    password character varying COLLATE pg_catalog."default",
    status boolean,
    user_type_id integer,
    CONSTRAINT user_pkey PRIMARY KEY (id),
    CONSTRAINT user_user_type_id_fkey FOREIGN KEY (user_type_id)
        REFERENCES public.user_type (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."user"
    OWNER to admin;
-- Index: ix_user_email

-- DROP INDEX IF EXISTS public.ix_user_email;

CREATE UNIQUE INDEX IF NOT EXISTS ix_user_email
    ON public."user" USING btree
    (email COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_user_id

-- DROP INDEX IF EXISTS public.ix_user_id;

CREATE INDEX IF NOT EXISTS ix_user_id
    ON public."user" USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
