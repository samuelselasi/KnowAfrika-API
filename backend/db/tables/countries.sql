-- Table: public.countries

-- DROP TABLE IF EXISTS public.countries;

CREATE TABLE IF NOT EXISTS public.countries
(
    id integer NOT NULL DEFAULT nextval('countries_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    region_id integer,
    CONSTRAINT countries_pkey PRIMARY KEY (id),
    CONSTRAINT countries_region_id_fkey FOREIGN KEY (region_id)
        REFERENCES public.regions (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.countries
    OWNER to admin;
-- Index: ix_countries_id

-- DROP INDEX IF EXISTS public.ix_countries_id;

CREATE INDEX IF NOT EXISTS ix_countries_id
    ON public.countries USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_countries_name

-- DROP INDEX IF EXISTS public.ix_countries_name;

CREATE INDEX IF NOT EXISTS ix_countries_name
    ON public.countries USING btree
    (name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
