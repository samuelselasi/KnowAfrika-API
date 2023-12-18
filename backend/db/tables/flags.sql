-- Table: public.flags

-- DROP TABLE IF EXISTS public.flags;

CREATE TABLE IF NOT EXISTS public.flags
(
    id integer NOT NULL DEFAULT nextval('flags_id_seq'::regclass),
    title character varying COLLATE pg_catalog."default",
    content bytea,
    country_id integer,
    CONSTRAINT flags_pkey PRIMARY KEY (id),
    CONSTRAINT flags_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.flags
    OWNER to admin;
-- Index: ix_flags_id

-- DROP INDEX IF EXISTS public.ix_flags_id;

CREATE INDEX IF NOT EXISTS ix_flags_id
    ON public.flags USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
