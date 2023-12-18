-- Table: public.regions

-- DROP TABLE IF EXISTS public.regions;

CREATE TABLE IF NOT EXISTS public.regions
(
    id integer NOT NULL DEFAULT nextval('regions_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default",
    is_active boolean,
    CONSTRAINT regions_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.regions
    OWNER to admin;
-- Index: ix_regions_id

-- DROP INDEX IF EXISTS public.ix_regions_id;

CREATE INDEX IF NOT EXISTS ix_regions_id
    ON public.regions USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: ix_regions_name

-- DROP INDEX IF EXISTS public.ix_regions_name;

CREATE UNIQUE INDEX IF NOT EXISTS ix_regions_name
    ON public.regions USING btree
    (name COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
