-- Table: public.transports

-- DROP TABLE IF EXISTS public.transports;

CREATE TABLE IF NOT EXISTS public.transports
(
    id integer NOT NULL DEFAULT nextval('transports_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    country_id integer,
    CONSTRAINT transports_pkey PRIMARY KEY (id),
    CONSTRAINT transports_country_id_fkey FOREIGN KEY (country_id)
        REFERENCES public.countries (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.transports
    OWNER to admin;
-- Index: ix_transports_id

-- DROP INDEX IF EXISTS public.ix_transports_id;

CREATE INDEX IF NOT EXISTS ix_transports_id
    ON public.transports USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
