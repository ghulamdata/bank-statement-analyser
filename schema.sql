
-- Bank Statement Analyser
-- PostgreSQL database table structure

CREATE TABLE IF NOT EXISTS public.transactions (

    transaction_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    transaction_date DATE NOT NULL,

    description VARCHAR(255),

    transaction_type VARCHAR(20),

    money_in NUMERIC(12,2),

    money_out NUMERIC(12,2),

    balance NUMERIC(12,2),

    category VARCHAR(100),

    statement_id VARCHAR(64),

    row_number INTEGER,

    CONSTRAINT unique_statement_transaction
        UNIQUE (statement_id, row_number)

);
