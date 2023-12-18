-- Table: public.user_info

-- DROP TABLE IF EXISTS public.user_info;

CREATE TABLE IF NOT EXISTS public.user_info
(
    id integer NOT NULL DEFAULT nextval('user_info_id_seq'::regclass),
    user_id integer,
    first_name character varying COLLATE pg_catalog."default",
    middle_name character varying COLLATE pg_catalog."default",
    last_name character varying COLLATE pg_catalog."default",
    CONSTRAINT user_info_pkey PRIMARY KEY (id),
    CONSTRAINT user_info_user_id_key UNIQUE (user_id),
    CONSTRAINT user_info_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_info
    OWNER to admin;
-- Index: ix_user_info_id

-- DROP INDEX IF EXISTS public.ix_user_info_id;

CREATE INDEX IF NOT EXISTS ix_user_info_id
    ON public.user_info USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
