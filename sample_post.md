# SaaS Monitoring Platform
My project models data for a SaaS Monitoring Platform to help them reduce their costs. It contains information about the subscriptions and their activity rates

<img src="schema.png">

## Query that I think perforemed well

Question: "Which SaaS providers are most popular across all clients?"
GPT SQL Query: "\nSELECT sp.provider_name, COUNT(s.subscription_id) AS subscription_count\nFROM SaaS_Providers sp\nJOIN Subscriptions s ON sp.provider_id = s.provider_id\nGROUP BY sp.provider_name\nORDER BY subscription_count DESC;\n",
Friendly Response: "The most popular SaaS providers are Microsoft 365, Zoom, Salesforce, Slack, and AWS!"

## Thoughts on the rest of the responses

It did not seem to have difficulty with the rest of the responses, it consistently gave answers that were correct.

# prompting strategies

I actually used all three strategies. I don't know if it's because the database was well designed and normalized, but I received consistent results.
Some of the queries added some details for clearer responses, but untilmately, it returned the same results.

For example, this is an example of the respponse to a question for all three of them:


### Cross Domain

{
"question": "Which clients have the most active subscriptions?",
"sql": "\nSELECT c.client_name, COUNT(s.subscription_id) AS active_subscriptions\nFROM Clients c\nJOIN Subscriptions s ON c.client_id = s.client_id\nWHERE s.subscription_status = 'Active'\nGROUP BY c.client_name\nORDER BY active_subscriptions DESC;\n",
"queryRawResponse": "[('Acme Corp', 2), ('Delta Enterprises', 1)]",
"friendlyResponse": "The clients with the most active subscriptions are Acme Corp with 2 subscriptions and Delta Enterprises with 1.",
"error": "None"
},

### Single Domain

{
"question": "Which clients have the most active subscriptions?",
"sql": "\nSELECT c.client_name, COUNT(s.subscription_id) AS active_subscriptions\nFROM Clients c\nJOIN Subscriptions s ON c.client_id = s.client_id\nWHERE s.subscription_status = 'Active'\nGROUP BY c.client_name\nORDER BY active_subscriptions DESC;\n",
"queryRawResponse": "[('Acme Corp', 2), ('Delta Enterprises', 1)]",
"friendlyResponse": "The clients with the most active subscriptions are Acme Corp with 2 subscriptions and Delta Enterprises with 1 subscription.",
"error": "None"
},

### Zero Shot
{
"question": "Which clients have the most active subscriptions?",
"sql": "\nSELECT c.client_id, c.client_name, COUNT(s.subscription_id) AS active_subscriptions\nFROM Clients c\nJOIN Subscriptions s ON c.client_id = s.client_id\nWHERE s.subscription_status = 'Active'\nGROUP BY c.client_id, c.client_name\nORDER BY active_subscriptions DESC;\n",
"queryRawResponse": "[(1, 'Acme Corp', 2), (4, 'Delta Enterprises', 1)]",
"friendlyResponse": "The clients with the most active subscriptions are Acme Corp with 2 subscriptions and Delta Enterprises with 1 subscription.",
"error": "None"
},

