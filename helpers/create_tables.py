import psycopg2

def create_prisma_migrations_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "_prisma_migrations" (
            "id" VARCHAR(36) PRIMARY KEY NOT NULL,
            "checksum" VARCHAR(64) NOT NULL,
            "finished_at" TIMESTAMPTZ(3) DEFAULT NULL,
            "migration_name" VARCHAR(255) NOT NULL,
            "logs" TEXT,
            "rolled_back_at" TIMESTAMPTZ(3) DEFAULT NULL,
            "started_at" TIMESTAMPTZ(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
            "applied_steps_count" INTEGER NOT NULL DEFAULT 0
        );
    """)

def create_user_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "user" (
            "user_id" UUID PRIMARY KEY,
            "username" VARCHAR(255) UNIQUE NOT NULL,
            "password" VARCHAR(60) NOT NULL,
            "role" VARCHAR(50) NOT NULL,
            "logo_url" VARCHAR(2183),
            "display_name" VARCHAR(255),
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "deleted_at" TIMESTAMPTZ(6),
            CONSTRAINT "user_username_unique" UNIQUE ("username")
        );
    """)

def create_team_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "team" (
            "team_id" UUID PRIMARY KEY,
            "name" VARCHAR(50) NOT NULL,
            "access_code" VARCHAR(50) UNIQUE,
            "logo_url" VARCHAR(2183),
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "deleted_at" TIMESTAMPTZ(6)
        );
    """)

def create_website_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "website" (
            "website_id" UUID PRIMARY KEY,
            "name" VARCHAR(100) NOT NULL,
            "domain" VARCHAR(500),
            "share_id" VARCHAR(50) UNIQUE,
            "reset_at" TIMESTAMPTZ(6),
            "user_id" UUID,
            "team_id" UUID,
            "created_by" UUID,
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "deleted_at" TIMESTAMPTZ(6),
            FOREIGN KEY ("user_id") REFERENCES "user"("user_id"),
            FOREIGN KEY ("created_by") REFERENCES "user"("user_id"),
            FOREIGN KEY ("team_id") REFERENCES "team"("team_id")
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_website_user_id ON "website"("user_id");
        CREATE INDEX idx_website_team_id ON "website"("team_id");
        CREATE INDEX idx_website_created_at ON "website"("created_at");
        CREATE INDEX idx_website_share_id ON "website"("share_id");
        CREATE INDEX idx_website_created_by ON "website"("created_by");
    """)

def create_session_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "session" (
            "session_id" UUID PRIMARY KEY,
            "website_id" UUID NOT NULL,
            "browser" VARCHAR(20),
            "os" VARCHAR(20),
            "device" VARCHAR(20),
            "screen" VARCHAR(11),
            "language" VARCHAR(35),
            "country" CHAR(2),
            "region" VARCHAR(20),
            "city" VARCHAR(50),
            "distinct_id" VARCHAR(50),
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("website_id") REFERENCES "website"("website_id")
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_session_created_at ON "session"("created_at");
        CREATE INDEX idx_session_website_id ON "session"("website_id");
    """)

def create_website_event_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "website_event" (
            "event_id" UUID PRIMARY KEY,
            "website_id" UUID NOT NULL,
            "session_id" UUID NOT NULL,
            "visit_id" UUID NOT NULL,
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "url_path" VARCHAR(500) NOT NULL,
            "url_query" VARCHAR(500),
            "utm_source" VARCHAR(255),
            "utm_medium" VARCHAR(255),
            "utm_campaign" VARCHAR(255),
            "utm_content" VARCHAR(255),
            "utm_term" VARCHAR(255),
            "referrer_path" VARCHAR(500),
            "referrer_query" VARCHAR(500),
            "referrer_domain" VARCHAR(500),
            "page_title" VARCHAR(500),
            "gclid" VARCHAR(255),
            "fbclid" VARCHAR(255),
            "msclkid" VARCHAR(255),
            "ttclid" VARCHAR(255),
            "li_fat_id" VARCHAR(255),
            "twclid" VARCHAR(255),
            "event_type" INTEGER DEFAULT 1,
            "event_name" VARCHAR(50),
            "tag" VARCHAR(50),
            "hostname" VARCHAR(100),
            FOREIGN KEY ("session_id") REFERENCES "session"("session_id")
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_website_event_created_at ON "website_event"("created_at");
        CREATE INDEX idx_website_event_session_id ON "website_event"("session_id");
        CREATE INDEX idx_website_event_website_id ON "website_event"("website_id");
    """)

def create_event_data_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "event_data" (
            "event_data_id" UUID PRIMARY KEY,
            "website_id" UUID NOT NULL,
            "website_event_id" UUID NOT NULL,
            "data_key" VARCHAR(500) NOT NULL,
            "string_value" VARCHAR(500),
            "number_value" DECIMAL(19, 4),
            "date_value" TIMESTAMPTZ(6),
            "data_type" INTEGER NOT NULL,
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("website_id") REFERENCES "website"("website_id"),
            FOREIGN KEY ("website_event_id") REFERENCES "website_event"("event_id")
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_event_data_created_at ON "event_data"("created_at");
        CREATE INDEX idx_event_data_website_id ON "event_data"("website_id");
    """)

def create_session_data_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "session_data" (
            "session_data_id" UUID PRIMARY KEY,
            "website_id" UUID NOT NULL,
            "session_id" UUID NOT NULL,
            "data_key" VARCHAR(500) NOT NULL,
            "string_value" VARCHAR(500),
            "number_value" DECIMAL(19, 4),
            "date_value" TIMESTAMPTZ(6),
            "data_type" INTEGER NOT NULL,
            "distinct_id" VARCHAR(50),
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("website_id") REFERENCES "website"("website_id"),
            FOREIGN KEY ("session_id") REFERENCES "session"("session_id")
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_session_data_created_at ON "session_data"("created_at");
        CREATE INDEX idx_session_data_website_id ON "session_data"("website_id");
    """)

def create_team_user_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "team_user" (
            "team_user_id" UUID PRIMARY KEY,
            "team_id" UUID NOT NULL,
            "user_id" UUID NOT NULL,
            "role" VARCHAR(50) NOT NULL,
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("team_id") REFERENCES "team"("team_id") ON DELETE CASCADE,
            FOREIGN KEY ("user_id") REFERENCES "user"("user_id") ON DELETE CASCADE
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_team_user_team_id ON "team_user"("team_id");
        CREATE INDEX idx_team_user_user_id ON "team_user"("user_id");
    """)

def create_report_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "report" (
            "report_id" UUID PRIMARY KEY,
            "user_id" UUID NOT NULL,
            "website_id" UUID NOT NULL,
            "type" VARCHAR(200) NOT NULL,
            "name" VARCHAR(200) NOT NULL,
            "description" VARCHAR(500) NOT NULL,
            "parameters" VARCHAR(6000) NOT NULL,
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("user_id") REFERENCES "user"("user_id") ON DELETE CASCADE,
            FOREIGN KEY ("website_id") REFERENCES "website"("website_id") ON DELETE CASCADE
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_report_user_id ON "report"("user_id");
        CREATE INDEX idx_report_website_id ON "report"("website_id");
    """)

def create_revenue_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "revenue" (
            "revenue_id" UUID PRIMARY KEY,
            "website_id" UUID NOT NULL,
            "session_id" UUID NOT NULL,
            "event_id" UUID NOT NULL,
            "event_name" VARCHAR(50) NOT NULL,
            "currency" VARCHAR(100) NOT NULL,
            "revenue" DECIMAL(19, 4),
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("website_id") REFERENCES "website"("website_id"),
            FOREIGN KEY ("session_id") REFERENCES "session"("session_id")
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_revenue_website_id ON "revenue"("website_id");
        CREATE INDEX idx_revenue_session_id ON "revenue"("session_id");
    """)

def create_segment_table(postgres_cursor):
    postgres_cursor.execute("""
        CREATE TABLE "segment" (
            "segment_id" UUID PRIMARY KEY,
            "website_id" UUID NOT NULL,
            "type" VARCHAR(200) NOT NULL,
            "name" VARCHAR(200) NOT NULL,
            "parameters" JSONB NOT NULL,
            "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY ("website_id") REFERENCES "website"("website_id") ON DELETE CASCADE
        );
    """)
    postgres_cursor.execute("""
        CREATE INDEX idx_segment_website_id ON "segment"("website_id");
    """)
