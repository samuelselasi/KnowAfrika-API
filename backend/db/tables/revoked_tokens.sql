-- Table: public.revoked_tokens

-- DROP TABLE IF EXISTS public.revoked_tokens;

CREATE TABLE IF NOT EXISTS public.revoked_tokens
(
    id integer NOT NULL DEFAULT nextval('revoked_tokens_id_seq'::regclass),
    jti character varying COLLATE pg_catalog."default",
    date_created timestamp without time zone,
    date_modified timestamp without time zone,
    CONSTRAINT revoked_tokens_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.revoked_tokens
    OWNER to admin;
