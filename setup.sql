CREATE TABLE IF NOT EXISTS Clients (
    client_id INTEGER PRIMARY KEY,
    client_name VARCHAR(50) NOT NULL,
    client_contact_email VARCHAR(50) NOT NULL,
    industry VARCHAR(50),
    signup_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS SaaS_Providers (
    provider_id INTEGER PRIMARY KEY,
    provider_name VARCHAR(50) NOT NULL,
    service_type VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS Subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    billing_cycle VARCHAR(20) NOT NULL, -- e.g., Monthly, Yearly
    subscription_cost DECIMAL(10, 2) NOT NULL,
    subscription_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients (client_id),
    FOREIGN KEY (provider_id) REFERENCES SaaS_Providers (provider_id)
);

CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    subscription_id INTEGER NOT NULL,
    invoice_date DATE NOT NULL,
    amount_due DECIMAL(10, 2) NOT NULL,
    due_date DATE NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients (client_id),
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions (subscription_id)
);

CREATE TABLE IF NOT EXISTS Usage_Logs (
    usage_id INTEGER PRIMARY KEY,
    subscription_id INTEGER NOT NULL,
    usage_date DATE NOT NULL,
    usage_metric VARCHAR(50) NOT NULL, -- e.g., GB used, minutes, etc.
    amount_used DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (subscription_id) REFERENCES Subscriptions (subscription_id)
);


CREATE TABLE IF NOT EXISTS Payment_Methods (
    payment_method_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    method_type VARCHAR(20) NOT NULL, -- e.g., Credit Card, Bank Transfer
    provider_name VARCHAR(50), -- Payment provider (e.g., Visa, MasterCard)
    last_four_digits CHAR(4), -- Last four digits of the card
    expiration_date DATE,
    FOREIGN KEY (client_id) REFERENCES Clients (client_id)
);
