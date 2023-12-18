-- Table: public.languages

-- DROP TABLE IF EXISTS public.languages;

CREATE TABLE IF NOT EXISTS public.languages
(
    id integer NOT NULL DEFAULT nextval('languages_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    form character varying COLLATE pg_catalog."default",
    country_id integer,
    CONSTRAINT languages_pkey PRIMARY KEY (id),
    CONSTRAINT languages_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.languages
    OWNER to admin;
-- Index: ix_languages_id

-- DROP INDEX IF EXISTS public.ix_languages_id;

CREATE INDEX IF NOT EXISTS ix_languages_id
    ON public.languages USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
