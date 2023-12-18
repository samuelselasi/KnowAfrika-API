-- Table: public.timezones

-- DROP TABLE IF EXISTS public.timezones;

CREATE TABLE IF NOT EXISTS public.timezones
(
    id integer NOT NULL DEFAULT nextval('timezones_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    country_id integer,
    CONSTRAINT timezones_pkey PRIMARY KEY (id),
    CONSTRAINT timezones_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.timezones
    OWNER to admin;
-- Index: ix_timezones_id

-- DROP INDEX IF EXISTS public.ix_timezones_id;

CREATE INDEX IF NOT EXISTS ix_timezones_id
    ON public.timezones USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
