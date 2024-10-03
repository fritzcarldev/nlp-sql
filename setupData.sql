
INSERT INTO Clients (client_id, client_name, client_contact_email, industry, signup_date, status) VALUES
(1, 'Acme Corp', 'contact@acmecorp.com', 'Manufacturing', '2022-01-15', 'Active'),
(2, 'Beta LLC', 'info@beta-llc.com', 'Finance', '2021-06-10', 'Active'),
(3, 'Gamma Technologies', 'support@gamma-tech.com', 'Technology', '2020-11-20', 'Inactive'),
(4, 'Delta Enterprises', 'sales@deltaenterprises.com', 'Retail', '2022-05-25', 'Active');


INSERT INTO SaaS_Providers (provider_id, provider_name, service_type) VALUES
(1, 'Zoom', 'Communication'),
(2, 'Salesforce', 'CRM'),
(3, 'AWS', 'Cloud Storage'),
(4, 'Microsoft 365', 'Productivity'),
(5, 'Slack', 'Communication');


INSERT INTO Subscriptions (subscription_id, client_id, provider_id, start_date, end_date, billing_cycle, subscription_cost, subscription_status) VALUES
(1, 1, 1, '2022-02-01', '2023-02-01', 'Yearly', 1500, 'Active'),
(2, 1, 2, '2022-03-15', '2023-03-15', 'Yearly', 2000, 'Active'),
(3, 2, 3, '2021-07-01', '2022-07-01', 'Yearly', 12000, 'Expired'),
(4, 3, 4, '2020-12-01', '2021-12-01', 'Monthly', 30, 'Canceled'),
(5, 4, 5, '2022-06-01', NULL, 'Monthly', 12, 'Active');

INSERT INTO Invoices (invoice_id, client_id, subscription_id, invoice_date, amount_due, due_date, payment_status) VALUES
(1, 1, 1, '2022-02-01', 1500, '2022-02-28', 'Paid'),
(2, 1, 2, '2022-03-15', 2000, '2022-04-15', 'Paid'),
(3, 2, 3, '2021-07-01', 12000, '2021-07-30', 'Unpaid'),
(4, 3, 4, '2020-12-01', 30, '2021-01-01', 'Paid'),
(5, 4, 5, '2022-06-01', 12, '2022-06-30', 'Paid');


INSERT INTO Usage_Logs (usage_id, subscription_id, usage_date, usage_metric, amount_used) VALUES
(1, 1, '2022-06-01', 'Minutes used', 500),
(2, 2, '2022-07-01', 'Records stored', 10000),
(3, 3, '2021-09-01', 'GB stored', 500),
(4, 4, '2020-12-15', 'Emails sent', 2000),
(5, 5, '2022-07-01', 'Messages sent', 3500);


INSERT INTO Payment_Methods (payment_method_id, client_id, method_type, provider_name, last_four_digits, expiration_date) VALUES
(1, 1, 'Credit Card', 'Visa', 1234, '2024-06-30'),
(2, 2, 'Credit Card', 'MasterCard', 5678, '2023-11-15'),
(3, 3, 'Bank Transfer', 'Chase Bank', NULL, NULL),
(4, 4, 'Credit Card', 'Amex', 9101, '2025-03-31');
