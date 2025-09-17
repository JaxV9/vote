import azure.functions as func
import datetime, json, logging, uuid


app = func.FunctionApp()

@app.function_name(name="postUser")
@app.route(route="postUser", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="user",
    create_if_not_exists=True
)
@app.cosmos_db_input(
    arg_name="existingUser",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="user",
    sql_query="SELECT * FROM c WHERE c.email = {email} OR c.pseudo = {pseudo}"
)
def postUser(req: func.HttpRequest, existingUser: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = req.get_json()
        pseudo = body.get("pseudo")
        email = body.get("email")
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if pseudo is None or email is None:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: date, pseudo, email"}),
                mimetype="application/json",
                status_code=400
            )
        
        if existingUser:
            return func.HttpResponse(
                json.dumps({"error": "User already exists"}),
                mimetype="application/json",
                status_code=403
            )
        document = {
            "id": str(uuid.uuid4()),
            "date": timestamp,
            "pseudo": pseudo,
            "email": email
        }
        outputDocument.set(func.Document.from_dict(document))
        return func.HttpResponse(
            json.dumps({"status": "saved", "document": document}),
            mimetype="application/json",
            status_code=201
        )
    
    except Exception as e:
        logging.error(f"Erreur lors de l’insertion : {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )

@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="user",
    create_if_not_exists=True
)
@app.cosmos_db_input(
    arg_name="existingUser",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="user",
    sql_query="SELECT c.id, c.pseudo, c.email FROM c WHERE c.id = {userId}"
)
@app.route(route="getUser", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def getUser(req: func.HttpRequest, existingUser: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:

    try:
        body = req.get_json()
        userId = body.get("userID")

        if not existingUser:
            return func.HttpResponse(
                json.dumps({"error": "User not found"}),
                mimetype="application/json",
                status_code=404
            )
        
        return func.HttpResponse(
            json.dumps({"document": existingUser[0].to_dict()}),
            mimetype="application/json",
            status_code=200
        )
    
    except Exception as e:
        logging.error(f"Erreur lors de l’insertion : {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )

@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="vote",
    create_if_not_exists=True
)
@app.cosmos_db_input(
    arg_name="existingUser",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="user",
    sql_query="SELECT * FROM c WHERE c.id = {userId}"
)
@app.route(route="postVote", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def postVote(req: func.HttpRequest, existingUser: func.DocumentList, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = req.get_json()
        userId = body.get("userId")
        vote = body.get("vote")
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if userId is None or vote is None:
            return func.HttpResponse(
                json.dumps({"error": "Missing required fields: date, pseudo, email"}),
                mimetype="application/json",
                status_code=400
            )
        
        if existingUser:
            return func.HttpResponse(
                json.dumps({"error": "User has already voted"}),
                mimetype="application/json",
                status_code=403
            )
        
        document = {
            "id": str(uuid.uuid4()),
            "date": timestamp,
            "userId": userId,
            "vote": vote
        }
        outputDocument.set(func.Document.from_dict(document))
        return func.HttpResponse(
            json.dumps({"status": "saved", "document": document}),
            mimetype="application/json",
            status_code=201
        )
    
    except Exception as e:
        logging.error(f"Erreur lors de l’insertion : {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )

@app.route(route="getVote", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def getVote(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )