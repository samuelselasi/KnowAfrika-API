-- Table: public.cities

-- DROP TABLE IF EXISTS public.cities;

CREATE TABLE IF NOT EXISTS public.cities
(
    id integer NOT NULL DEFAULT nextval('cities_id_seq'::regclass),
    country_id integer,
    province_id integer,
    name character varying COLLATE pg_catalog."default",
    CONSTRAINT cities_pkey PRIMARY KEY (id),
    CONSTRAINT cities_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT cities_province_id_fkey FOREIGN KEY (province_id)
        REFERENCES public.provinces (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.cities
    OWNER to admin;
-- Index: ix_cities_id

-- DROP INDEX IF EXISTS public.ix_cities_id;

CREATE INDEX IF NOT EXISTS ix_cities_id
    ON public.cities USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_cities_name

-- DROP INDEX IF EXISTS public.ix_cities_name;

CREATE INDEX IF NOT EXISTS ix_cities_name
    ON public.cities USING btree
    (name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
