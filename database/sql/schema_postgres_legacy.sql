--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8
-- Dumped by pg_dump version 16.8

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: belirti_tanimlari; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.belirti_tanimlari (
    id integer NOT NULL,
    ad character varying(100) NOT NULL,
    CONSTRAINT belirti_tanimlari_ad_check CHECK (((ad)::text = ANY ((ARRAY['Poliüri (Sık idrara çıkma)'::character varying, 'Polifaji (Aşırı açlık hissi)'::character varying, 'Polidipsi (Aşırı susama hissi)'::character varying, 'Nöropati (El ve ayaklarda karıncalanma veya uyuşma hissi)'::character varying, 'Kilo kaybı'::character varying, 'Yorgunluk'::character varying, 'Yaraların yavaş iyileşmesi'::character varying, 'Bulanık görme'::character varying])::text[])))
);


ALTER TABLE public.belirti_tanimlari OWNER TO postgres;

--
-- Name: belirti_tanimlari_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.belirti_tanimlari_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.belirti_tanimlari_id_seq OWNER TO postgres;

--
-- Name: belirti_tanimlari_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.belirti_tanimlari_id_seq OWNED BY public.belirti_tanimlari.id;


--
-- Name: belirtiler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.belirtiler (
    id integer NOT NULL,
    hasta_id integer NOT NULL,
    tarih_zaman timestamp with time zone DEFAULT now() NOT NULL,
    belirti_id integer NOT NULL
);


ALTER TABLE public.belirtiler OWNER TO postgres;

--
-- Name: belirtiler_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.belirtiler_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.belirtiler_id_seq OWNER TO postgres;

--
-- Name: belirtiler_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.belirtiler_id_seq OWNED BY public.belirtiler.id;


--
-- Name: diyet_tanimlari; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.diyet_tanimlari (
    id integer NOT NULL,
    ad character varying(50) NOT NULL,
    CONSTRAINT diyet_tanimlari_ad_check CHECK (((ad)::text = ANY ((ARRAY['Az Şekerli Diyet'::character varying, 'Şekersiz Diyet'::character varying, 'Dengeli Beslenme'::character varying])::text[])))
);


ALTER TABLE public.diyet_tanimlari OWNER TO postgres;

--
-- Name: diyet_tanimlari_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.diyet_tanimlari_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.diyet_tanimlari_id_seq OWNER TO postgres;

--
-- Name: diyet_tanimlari_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.diyet_tanimlari_id_seq OWNED BY public.diyet_tanimlari.id;


--
-- Name: diyetler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.diyetler (
    id integer NOT NULL,
    hasta_id integer NOT NULL,
    tarih_zaman timestamp with time zone DEFAULT now() NOT NULL,
    diyet_id integer NOT NULL,
    durum character varying(20) NOT NULL,
    CONSTRAINT diyetler_durum_check CHECK (((durum)::text = ANY ((ARRAY['uygulandı'::character varying, 'uygulanmadı'::character varying])::text[])))
);


ALTER TABLE public.diyetler OWNER TO postgres;

--
-- Name: diyetler_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.diyetler_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.diyetler_id_seq OWNER TO postgres;

--
-- Name: diyetler_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.diyetler_id_seq OWNED BY public.diyetler.id;


--
-- Name: doktorlar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.doktorlar (
    id integer NOT NULL,
    tc character varying(11) NOT NULL,
    ad character varying(50) NOT NULL,
    soyad character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    sifre bytea NOT NULL,
    dogum_tarihi date NOT NULL,
    cinsiyet character varying(10) NOT NULL,
    profil_resmi bytea,
    uzmanlik_alani character varying(100) NOT NULL,
    CONSTRAINT doktorlar_ad_check CHECK (((ad)::text ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'::text)),
    CONSTRAINT doktorlar_cinsiyet_check CHECK (((cinsiyet)::text = ANY ((ARRAY['Erkek'::character varying, 'Kadın'::character varying, 'Diğer'::character varying])::text[]))),
    CONSTRAINT doktorlar_email_check CHECK (((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'::text)),
    CONSTRAINT doktorlar_soyad_check CHECK (((soyad)::text ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'::text)),
    CONSTRAINT doktorlar_tc_check CHECK (((tc)::text ~ '^[0-9]{11}$'::text)),
    CONSTRAINT doktorlar_uzmanlik_alani_check CHECK (((uzmanlik_alani)::text ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ\s]+$'::text))
);


ALTER TABLE public.doktorlar OWNER TO postgres;

--
-- Name: doktorlar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.doktorlar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.doktorlar_id_seq OWNER TO postgres;

--
-- Name: doktorlar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.doktorlar_id_seq OWNED BY public.doktorlar.id;


--
-- Name: egzersiz_durumlari; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.egzersiz_durumlari (
    id integer NOT NULL,
    durum_adi character varying(20) NOT NULL,
    CONSTRAINT egzersiz_durumlari_durum_adi_check CHECK (((durum_adi)::text = ANY ((ARRAY['yapıldı'::character varying, 'yapılmadı'::character varying])::text[])))
);


ALTER TABLE public.egzersiz_durumlari OWNER TO postgres;

--
-- Name: egzersiz_durumlari_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.egzersiz_durumlari_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.egzersiz_durumlari_id_seq OWNER TO postgres;

--
-- Name: egzersiz_durumlari_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.egzersiz_durumlari_id_seq OWNED BY public.egzersiz_durumlari.id;


--
-- Name: egzersiz_turleri; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.egzersiz_turleri (
    id integer NOT NULL,
    tur_adi character varying(50) NOT NULL,
    CONSTRAINT egzersiz_turleri_tur_adi_check CHECK (((tur_adi)::text = ANY ((ARRAY['Yürüyüş'::character varying, 'Klinik Egzersiz'::character varying, 'Bisiklet'::character varying])::text[])))
);


ALTER TABLE public.egzersiz_turleri OWNER TO postgres;

--
-- Name: egzersiz_turleri_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.egzersiz_turleri_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.egzersiz_turleri_id_seq OWNER TO postgres;

--
-- Name: egzersiz_turleri_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.egzersiz_turleri_id_seq OWNED BY public.egzersiz_turleri.id;


--
-- Name: egzersizler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.egzersizler (
    id integer NOT NULL,
    hasta_id integer NOT NULL,
    tarih_zaman timestamp with time zone DEFAULT now() NOT NULL,
    tur_id integer NOT NULL,
    durum_id integer NOT NULL
);


ALTER TABLE public.egzersizler OWNER TO postgres;

--
-- Name: egzersizler_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.egzersizler_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.egzersizler_id_seq OWNER TO postgres;

--
-- Name: egzersizler_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.egzersizler_id_seq OWNED BY public.egzersizler.id;


--
-- Name: hastalar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hastalar (
    id integer NOT NULL,
    tc character varying(11) NOT NULL,
    ad character varying(50) NOT NULL,
    soyad character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    sifre bytea NOT NULL,
    dogum_tarihi date NOT NULL,
    cinsiyet character varying(10) NOT NULL,
    profil_resmi bytea,
    doktor_id integer NOT NULL,
    CONSTRAINT hastalar_ad_check CHECK (((ad)::text ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'::text)),
    CONSTRAINT hastalar_cinsiyet_check CHECK (((cinsiyet)::text = ANY ((ARRAY['Erkek'::character varying, 'Kadın'::character varying, 'Diğer'::character varying])::text[]))),
    CONSTRAINT hastalar_email_check CHECK (((email)::text ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'::text)),
    CONSTRAINT hastalar_soyad_check CHECK (((soyad)::text ~* '^[a-zA-ZçğıöşüÇĞİÖŞÜ]+$'::text)),
    CONSTRAINT hastalar_tc_check CHECK (((tc)::text ~ '^[0-9]{11}$'::text))
);


ALTER TABLE public.hastalar OWNER TO postgres;

--
-- Name: hastalar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hastalar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hastalar_id_seq OWNER TO postgres;

--
-- Name: hastalar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hastalar_id_seq OWNED BY public.hastalar.id;


--
-- Name: kan_sekeri; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kan_sekeri (
    id integer NOT NULL,
    hasta_id integer NOT NULL,
    tarih_zaman timestamp with time zone DEFAULT now() NOT NULL,
    kan_sekeri integer NOT NULL,
    olcum_grubu character varying(10),
    CONSTRAINT kan_sekeri_kan_sekeri_check CHECK (((kan_sekeri >= 20) AND (kan_sekeri <= 500))),
    CONSTRAINT olcum_grubu_check CHECK (((olcum_grubu)::text = ANY ((ARRAY['sabah'::character varying, 'öğle'::character varying, 'ikindi'::character varying, 'akşam'::character varying, 'gece'::character varying])::text[])))
);


ALTER TABLE public.kan_sekeri OWNER TO postgres;

--
-- Name: kan_sekeri_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kan_sekeri_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.kan_sekeri_id_seq OWNER TO postgres;

--
-- Name: kan_sekeri_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kan_sekeri_id_seq OWNED BY public.kan_sekeri.id;


--
-- Name: notlar_ve_oneriler; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notlar_ve_oneriler (
    id integer NOT NULL,
    hasta_id integer NOT NULL,
    doktor_id integer NOT NULL,
    tarih timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    baslik text,
    aciklama text
);


ALTER TABLE public.notlar_ve_oneriler OWNER TO postgres;

--
-- Name: notlar_ve_oneriler_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notlar_ve_oneriler_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notlar_ve_oneriler_id_seq OWNER TO postgres;

--
-- Name: notlar_ve_oneriler_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notlar_ve_oneriler_id_seq OWNED BY public.notlar_ve_oneriler.id;


--
-- Name: uyari_turleri; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.uyari_turleri (
    id integer NOT NULL,
    tip character varying(50) NOT NULL
);


ALTER TABLE public.uyari_turleri OWNER TO postgres;

--
-- Name: uyari_turleri_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.uyari_turleri_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.uyari_turleri_id_seq OWNER TO postgres;

--
-- Name: uyari_turleri_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.uyari_turleri_id_seq OWNED BY public.uyari_turleri.id;


--
-- Name: uyarilar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.uyarilar (
    id integer NOT NULL,
    hasta_id integer NOT NULL,
    zaman timestamp with time zone DEFAULT now() NOT NULL,
    tip_id integer NOT NULL,
    mesaj text NOT NULL
);


ALTER TABLE public.uyarilar OWNER TO postgres;

--
-- Name: uyarilar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.uyarilar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.uyarilar_id_seq OWNER TO postgres;

--
-- Name: uyarilar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.uyarilar_id_seq OWNED BY public.uyarilar.id;


--
-- Name: belirti_tanimlari id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirti_tanimlari ALTER COLUMN id SET DEFAULT nextval('public.belirti_tanimlari_id_seq'::regclass);


--
-- Name: belirtiler id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirtiler ALTER COLUMN id SET DEFAULT nextval('public.belirtiler_id_seq'::regclass);


--
-- Name: diyet_tanimlari id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyet_tanimlari ALTER COLUMN id SET DEFAULT nextval('public.diyet_tanimlari_id_seq'::regclass);


--
-- Name: diyetler id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyetler ALTER COLUMN id SET DEFAULT nextval('public.diyetler_id_seq'::regclass);


--
-- Name: doktorlar id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doktorlar ALTER COLUMN id SET DEFAULT nextval('public.doktorlar_id_seq'::regclass);


--
-- Name: egzersiz_durumlari id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz_durumlari ALTER COLUMN id SET DEFAULT nextval('public.egzersiz_durumlari_id_seq'::regclass);


--
-- Name: egzersiz_turleri id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz_turleri ALTER COLUMN id SET DEFAULT nextval('public.egzersiz_turleri_id_seq'::regclass);


--
-- Name: egzersizler id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersizler ALTER COLUMN id SET DEFAULT nextval('public.egzersizler_id_seq'::regclass);


--
-- Name: hastalar id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hastalar ALTER COLUMN id SET DEFAULT nextval('public.hastalar_id_seq'::regclass);


--
-- Name: kan_sekeri id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kan_sekeri ALTER COLUMN id SET DEFAULT nextval('public.kan_sekeri_id_seq'::regclass);


--
-- Name: notlar_ve_oneriler id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notlar_ve_oneriler ALTER COLUMN id SET DEFAULT nextval('public.notlar_ve_oneriler_id_seq'::regclass);


--
-- Name: uyari_turleri id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyari_turleri ALTER COLUMN id SET DEFAULT nextval('public.uyari_turleri_id_seq'::regclass);


--
-- Name: uyarilar id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyarilar ALTER COLUMN id SET DEFAULT nextval('public.uyarilar_id_seq'::regclass);


--
-- Name: belirti_tanimlari belirti_tanimlari_ad_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirti_tanimlari
    ADD CONSTRAINT belirti_tanimlari_ad_key UNIQUE (ad);


--
-- Name: belirti_tanimlari belirti_tanimlari_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirti_tanimlari
    ADD CONSTRAINT belirti_tanimlari_pkey PRIMARY KEY (id);


--
-- Name: belirtiler belirtiler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirtiler
    ADD CONSTRAINT belirtiler_pkey PRIMARY KEY (id);


--
-- Name: diyet_tanimlari diyet_tanimlari_ad_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyet_tanimlari
    ADD CONSTRAINT diyet_tanimlari_ad_key UNIQUE (ad);


--
-- Name: diyet_tanimlari diyet_tanimlari_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyet_tanimlari
    ADD CONSTRAINT diyet_tanimlari_pkey PRIMARY KEY (id);


--
-- Name: diyetler diyetler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyetler
    ADD CONSTRAINT diyetler_pkey PRIMARY KEY (id);


--
-- Name: doktorlar doktorlar_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doktorlar
    ADD CONSTRAINT doktorlar_email_key UNIQUE (email);


--
-- Name: doktorlar doktorlar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doktorlar
    ADD CONSTRAINT doktorlar_pkey PRIMARY KEY (id);


--
-- Name: doktorlar doktorlar_tc_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.doktorlar
    ADD CONSTRAINT doktorlar_tc_key UNIQUE (tc);


--
-- Name: egzersiz_durumlari egzersiz_durumlari_durum_adi_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz_durumlari
    ADD CONSTRAINT egzersiz_durumlari_durum_adi_key UNIQUE (durum_adi);


--
-- Name: egzersiz_durumlari egzersiz_durumlari_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz_durumlari
    ADD CONSTRAINT egzersiz_durumlari_pkey PRIMARY KEY (id);


--
-- Name: egzersiz_turleri egzersiz_turleri_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz_turleri
    ADD CONSTRAINT egzersiz_turleri_pkey PRIMARY KEY (id);


--
-- Name: egzersiz_turleri egzersiz_turleri_tur_adi_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersiz_turleri
    ADD CONSTRAINT egzersiz_turleri_tur_adi_key UNIQUE (tur_adi);


--
-- Name: egzersizler egzersizler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersizler
    ADD CONSTRAINT egzersizler_pkey PRIMARY KEY (id);


--
-- Name: hastalar hastalar_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hastalar
    ADD CONSTRAINT hastalar_email_key UNIQUE (email);


--
-- Name: hastalar hastalar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hastalar
    ADD CONSTRAINT hastalar_pkey PRIMARY KEY (id);


--
-- Name: hastalar hastalar_tc_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hastalar
    ADD CONSTRAINT hastalar_tc_key UNIQUE (tc);


--
-- Name: kan_sekeri kan_sekeri_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kan_sekeri
    ADD CONSTRAINT kan_sekeri_pkey PRIMARY KEY (id);


--
-- Name: notlar_ve_oneriler notlar_ve_oneriler_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notlar_ve_oneriler
    ADD CONSTRAINT notlar_ve_oneriler_pkey PRIMARY KEY (id);


--
-- Name: uyari_turleri uyari_turleri_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyari_turleri
    ADD CONSTRAINT uyari_turleri_pkey PRIMARY KEY (id);


--
-- Name: uyari_turleri uyari_turleri_tip_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyari_turleri
    ADD CONSTRAINT uyari_turleri_tip_key UNIQUE (tip);


--
-- Name: uyarilar uyarilar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyarilar
    ADD CONSTRAINT uyarilar_pkey PRIMARY KEY (id);


--
-- Name: belirtiler belirtiler_belirti_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirtiler
    ADD CONSTRAINT belirtiler_belirti_id_fkey FOREIGN KEY (belirti_id) REFERENCES public.belirti_tanimlari(id) ON DELETE CASCADE;


--
-- Name: belirtiler belirtiler_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.belirtiler
    ADD CONSTRAINT belirtiler_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.hastalar(id) ON DELETE CASCADE;


--
-- Name: diyetler diyetler_diyet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyetler
    ADD CONSTRAINT diyetler_diyet_id_fkey FOREIGN KEY (diyet_id) REFERENCES public.diyet_tanimlari(id) ON DELETE CASCADE;


--
-- Name: diyetler diyetler_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.diyetler
    ADD CONSTRAINT diyetler_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.hastalar(id) ON DELETE CASCADE;


--
-- Name: egzersizler egzersizler_durum_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersizler
    ADD CONSTRAINT egzersizler_durum_id_fkey FOREIGN KEY (durum_id) REFERENCES public.egzersiz_durumlari(id);


--
-- Name: egzersizler egzersizler_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersizler
    ADD CONSTRAINT egzersizler_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.hastalar(id) ON DELETE CASCADE;


--
-- Name: egzersizler egzersizler_tur_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.egzersizler
    ADD CONSTRAINT egzersizler_tur_id_fkey FOREIGN KEY (tur_id) REFERENCES public.egzersiz_turleri(id);


--
-- Name: hastalar hastalar_doktor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hastalar
    ADD CONSTRAINT hastalar_doktor_id_fkey FOREIGN KEY (doktor_id) REFERENCES public.doktorlar(id) ON DELETE CASCADE;


--
-- Name: kan_sekeri kan_sekeri_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kan_sekeri
    ADD CONSTRAINT kan_sekeri_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.hastalar(id) ON DELETE CASCADE;


--
-- Name: notlar_ve_oneriler notlar_ve_oneriler_doktor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notlar_ve_oneriler
    ADD CONSTRAINT notlar_ve_oneriler_doktor_id_fkey FOREIGN KEY (doktor_id) REFERENCES public.doktorlar(id) ON DELETE CASCADE;


--
-- Name: notlar_ve_oneriler notlar_ve_oneriler_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notlar_ve_oneriler
    ADD CONSTRAINT notlar_ve_oneriler_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.hastalar(id) ON DELETE CASCADE;


--
-- Name: uyarilar uyarilar_hasta_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyarilar
    ADD CONSTRAINT uyarilar_hasta_id_fkey FOREIGN KEY (hasta_id) REFERENCES public.hastalar(id) ON DELETE CASCADE;


--
-- Name: uyarilar uyarilar_tip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.uyarilar
    ADD CONSTRAINT uyarilar_tip_id_fkey FOREIGN KEY (tip_id) REFERENCES public.uyari_turleri(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

