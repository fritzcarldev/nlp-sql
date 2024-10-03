import json
from openai import OpenAI
import os
import psycopg2
from time import time

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

configPath = getPath("config.json")
with open(configPath) as configFile:
    config = json.load(configFile)

connection_string = config.get("timescale_connection_string", 
    "postgresql://username:password@localhost:5432/dbname")

try:
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
except psycopg2.Error as e:
    print(f"Error connecting to TimescaleDB: {e}")
    exit(1)

setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

def truncate_tables(cursor):
    cursor.execute("TRUNCATE TABLE Usage_Logs CASCADE;")
    cursor.execute("TRUNCATE TABLE Invoices CASCADE;")
    cursor.execute("TRUNCATE TABLE Subscriptions CASCADE;")
    cursor.execute("TRUNCATE TABLE Payment_Methods CASCADE;")
    cursor.execute("TRUNCATE TABLE SaaS_Providers CASCADE;")
    cursor.execute("TRUNCATE TABLE Clients CASCADE;")

truncate_tables(cursor)

with open(setupSqlPath) as setupSqlFile, open(setupSqlDataPath) as setupSqlDataFile:
    setupSqlScript = setupSqlFile.read()
    setupSqlDataScript = setupSqlDataFile.read()

cursor.execute(setupSqlScript)
cursor.execute(setupSqlDataScript)
conn.commit()

def runSql(query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
        return None

# OPENAI
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(
    api_key = config["openaiKey"],
    organization = config["orgId"]
)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result


# strategies
commonSqlOnlyRequest = " Give me a PostgreSQL select statement that answers the question. Only respond with PostgreSQL syntax. If there is an error do not explain it!"

strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    
    "single_domain_double_shot": (setupSqlScript + 
                   " Which clients have subscriptions set to expire within the next 30 days? " + 
                   " \nSELECT client_name, provider_name, end_date\n" + 
                   "FROM Clients c\nJOIN Subscriptions s ON c.client_id = s.client_id\n" + 
                   "JOIN SaaS_Providers sp ON s.provider_id = sp.provider_id\n" + 
                   "WHERE s.end_date BETWEEN NOW() AND NOW() + INTERVAL '30 days';\n" + 
                   commonSqlOnlyRequest),
    "cross_domain_few_shot" : (
    setupSqlScript + 
    " In an e-commerce database, what are the top-selling products?\n" +
    " SELECT product_name, SUM(quantity_sold) AS total_sold\n" +
    " FROM Sales\n" +
    " GROUP BY product_name\n" +
    " ORDER BY total_sold DESC;\n" +
    
    " How many customers have made more than 5 purchases?\n" +
    " SELECT customer_id, COUNT(order_id) AS purchase_count\n" +
    " FROM Orders\n" +
    " GROUP BY customer_id\n" +
    " HAVING COUNT(order_id) > 5;\n" +
    
    " What is the average order value?\n" +
    " SELECT AVG(order_value) AS average_value\n" +
    " FROM Orders;\n" +
    
    " Now, which clients have subscriptions that are currently active?\n" +
    " SELECT c.client_name, COUNT(s.subscription_id) AS active_subscriptions\n" +
    " FROM Clients c\n" +
    " JOIN Subscriptions s ON c.client_id = s.client_id\n" +
    " WHERE s.subscription_status = 'Active'\n" +
    " GROUP BY c.client_name;\n" +
    
    commonSqlOnlyRequest
)
}


questions = [
    "Which clients have the most active subscriptions?",
    "Which SaaS providers are most popular across all clients?",
    "What are the total subscription costs for each client?",
    "Which clients are currently overdue on payments?",
    "What are the top 3 most subscribed-to SaaS providers?",
    "Which subscriptions are set to expire within the next 30 days?",
    "Which clients have multiple payment methods?",
    "How many active subscriptions does each client have?",
    "What is the average subscription cost per SaaS provider?",
    "Which clients have never had an unpaid invoice?",
    "Which clients have the highest total usage on their subscriptions?",
    "Which clients have canceled subscriptions in the past year?",
    "What is the total revenue generated from subscriptions per month?",
    "What are the total subscription costs for clients in the 'Technology' industry?",
    "Which clients are subscribed to multiple communication services (e.g., Zoom, Slack)?"
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question +"\" and the response was \""+queryRawResponse+"\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question, 
            "sql": sqlSyntaxResponse, 
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)
            

cursor.close()
conn.close()
print("Done!")