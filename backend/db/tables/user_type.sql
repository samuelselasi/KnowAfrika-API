-- Table: public.user_type

-- DROP TABLE IF EXISTS public.user_type;

CREATE TABLE IF NOT EXISTS public.user_type
(
    id integer NOT NULL DEFAULT nextval('user_type_id_seq'::regclass),
    title character varying COLLATE pg_catalog."default",
    CONSTRAINT user_type_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_type
    OWNER to admin;
-- Index: ix_user_type_id

-- DROP INDEX IF EXISTS public.ix_user_type_id;

CREATE INDEX IF NOT EXISTS ix_user_type_id
    ON public.user_type USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_user_type_title

-- DROP INDEX IF EXISTS public.ix_user_type_title;

CREATE UNIQUE INDEX IF NOT EXISTS ix_user_type_title
    ON public.user_type USING btree
    (title COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
