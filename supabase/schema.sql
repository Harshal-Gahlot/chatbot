


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


COMMENT ON SCHEMA "public" IS 'standard public schema';



CREATE EXTENSION IF NOT EXISTS "pg_stat_statements" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "pgcrypto" WITH SCHEMA "extensions";






CREATE EXTENSION IF NOT EXISTS "supabase_vault" WITH SCHEMA "vault";






CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA "extensions";





SET default_tablespace = '';

SET default_table_access_method = "heap";


CREATE TABLE IF NOT EXISTS "public"."elements" (
    "id" "uuid" NOT NULL,
    "threadId" "uuid",
    "type" "text",
    "url" "text",
    "chainlitKey" "text",
    "name" "text" NOT NULL,
    "display" "text",
    "objectKey" "text",
    "size" "text",
    "page" integer,
    "language" "text",
    "forId" "uuid",
    "mime" "text",
    "props" "jsonb"
);


ALTER TABLE "public"."elements" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."feedbacks" (
    "id" "uuid" NOT NULL,
    "forId" "uuid" NOT NULL,
    "threadId" "uuid" NOT NULL,
    "value" integer NOT NULL,
    "comment" "text"
);


ALTER TABLE "public"."feedbacks" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."steps" (
    "id" "uuid" NOT NULL,
    "name" "text" NOT NULL,
    "type" "text" NOT NULL,
    "threadId" "uuid" NOT NULL,
    "parentId" "uuid",
    "streaming" boolean NOT NULL,
    "waitForAnswer" boolean,
    "isError" boolean,
    "metadata" "jsonb",
    "tags" "text"[],
    "input" "text",
    "output" "text",
    "createdAt" "text",
    "command" "text",
    "start" "text",
    "end" "text",
    "generation" "jsonb",
    "showInput" "text",
    "language" "text",
    "indent" integer,
    "defaultOpen" boolean,
    "modes" "jsonb",
    "autoCollapse" boolean DEFAULT false NOT NULL
);


ALTER TABLE "public"."steps" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."threads" (
    "id" "uuid" NOT NULL,
    "createdAt" "text",
    "name" "text",
    "userId" "uuid",
    "userIdentifier" "text",
    "tags" "text"[],
    "metadata" "jsonb"
);


ALTER TABLE "public"."threads" OWNER TO "postgres";


CREATE TABLE IF NOT EXISTS "public"."users" (
    "id" "uuid" NOT NULL,
    "identifier" "text" NOT NULL,
    "metadata" "jsonb" NOT NULL,
    "createdAt" "text"
);


ALTER TABLE "public"."users" OWNER TO "postgres";


ALTER TABLE ONLY "public"."elements"
    ADD CONSTRAINT "elements_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."feedbacks"
    ADD CONSTRAINT "feedbacks_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."steps"
    ADD CONSTRAINT "steps_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."threads"
    ADD CONSTRAINT "threads_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_identifier_key" UNIQUE ("identifier");



ALTER TABLE ONLY "public"."users"
    ADD CONSTRAINT "users_pkey" PRIMARY KEY ("id");



ALTER TABLE ONLY "public"."elements"
    ADD CONSTRAINT "elements_threadId_fkey" FOREIGN KEY ("threadId") REFERENCES "public"."threads"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."feedbacks"
    ADD CONSTRAINT "feedbacks_threadId_fkey" FOREIGN KEY ("threadId") REFERENCES "public"."threads"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."steps"
    ADD CONSTRAINT "steps_threadId_fkey" FOREIGN KEY ("threadId") REFERENCES "public"."threads"("id") ON DELETE CASCADE;



ALTER TABLE ONLY "public"."threads"
    ADD CONSTRAINT "threads_userId_fkey" FOREIGN KEY ("userId") REFERENCES "public"."users"("id") ON DELETE CASCADE;



ALTER TABLE "public"."elements" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."feedbacks" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."steps" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."threads" ENABLE ROW LEVEL SECURITY;


ALTER TABLE "public"."users" ENABLE ROW LEVEL SECURITY;




ALTER PUBLICATION "supabase_realtime" OWNER TO "postgres";


GRANT USAGE ON SCHEMA "public" TO "postgres";
GRANT USAGE ON SCHEMA "public" TO "anon";
GRANT USAGE ON SCHEMA "public" TO "authenticated";
GRANT USAGE ON SCHEMA "public" TO "service_role";





































































































































































GRANT ALL ON TABLE "public"."elements" TO "anon";
GRANT ALL ON TABLE "public"."elements" TO "authenticated";
GRANT ALL ON TABLE "public"."elements" TO "service_role";



GRANT ALL ON TABLE "public"."feedbacks" TO "anon";
GRANT ALL ON TABLE "public"."feedbacks" TO "authenticated";
GRANT ALL ON TABLE "public"."feedbacks" TO "service_role";



GRANT ALL ON TABLE "public"."steps" TO "anon";
GRANT ALL ON TABLE "public"."steps" TO "authenticated";
GRANT ALL ON TABLE "public"."steps" TO "service_role";



GRANT ALL ON TABLE "public"."threads" TO "anon";
GRANT ALL ON TABLE "public"."threads" TO "authenticated";
GRANT ALL ON TABLE "public"."threads" TO "service_role";



GRANT ALL ON TABLE "public"."users" TO "anon";
GRANT ALL ON TABLE "public"."users" TO "authenticated";
GRANT ALL ON TABLE "public"."users" TO "service_role";









ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON SEQUENCES TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON FUNCTIONS TO "service_role";






ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "postgres";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "anon";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "authenticated";
ALTER DEFAULT PRIVILEGES FOR ROLE "postgres" IN SCHEMA "public" GRANT ALL ON TABLES TO "service_role";































