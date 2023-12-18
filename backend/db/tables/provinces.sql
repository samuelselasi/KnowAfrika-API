-- Table: public.provinces

-- DROP TABLE IF EXISTS public.provinces;

CREATE TABLE IF NOT EXISTS public.provinces
(
    id integer NOT NULL DEFAULT nextval('provinces_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    country_id integer,
    CONSTRAINT provinces_pkey PRIMARY KEY (id),
    CONSTRAINT provinces_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.provinces
    OWNER to admin;
-- Index: ix_provinces_id

-- DROP INDEX IF EXISTS public.ix_provinces_id;

CREATE INDEX IF NOT EXISTS ix_provinces_id
    ON public.provinces USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
