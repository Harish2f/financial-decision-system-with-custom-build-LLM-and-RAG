CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    country TEXT,
    industry TEXT,
    signup_date DATE,
    credit_limit FLOAT
);

CREATE TABLE contracts (
    contract_id TEXT PRIMARY KEY,
    customer_id TEXT,
    start_date DATE,
    end_date DATE,
    monthly_value FLOAT,
    sla_days INT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE invoices (
    invoice_id TEXT PRIMARY KEY,
    customer_id TEXT,
    contract_id TEXT,
    issue_date DATE,
    due_date DATE,
    amount FLOAT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY(contract_id) REFERENCES contracts(contract_id)
);

CREATE TABLE payments (
    payment_id TEXT PRIMARY KEY,
    invoice_id TEXT,
    payment_date DATE,
    amount_paid FLOAT,
    FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id)
);
