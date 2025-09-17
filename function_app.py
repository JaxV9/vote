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


@app.cosmos_db_input(
    arg_name="existingUser",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="user",
    sql_query="SELECT c.id, c.pseudo, c.email FROM c WHERE c.email = {email}"
)
@app.route(route="getUser", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def getUser(req: func.HttpRequest, existingUser: func.DocumentList) -> func.HttpResponse:

    try:
        body = req.get_json()

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
    container_name="vote",
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


@app.cosmos_db_input(
    arg_name="votesList",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="vote",
    sql_query="SELECT c.id, c.date, c.userId, c.vote FROM c"
)
@app.route(route="getVote", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def getVote(req: func.HttpRequest, votesList: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        return func.HttpResponse(
            json.dumps({"documents": [doc.to_dict() for doc in votesList]}),
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