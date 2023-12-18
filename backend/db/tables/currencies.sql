-- Table: public.currencies

-- DROP TABLE IF EXISTS public.currencies;

CREATE TABLE IF NOT EXISTS public.currencies
(
    id integer NOT NULL DEFAULT nextval('currencies_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    symbol character varying COLLATE pg_catalog."default",
    country_id integer,
    CONSTRAINT currencies_pkey PRIMARY KEY (id),
    CONSTRAINT currencies_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.currencies
    OWNER to admin;
-- Index: ix_currencies_id

-- DROP INDEX IF EXISTS public.ix_currencies_id;

CREATE INDEX IF NOT EXISTS ix_currencies_id
    ON public.currencies USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
