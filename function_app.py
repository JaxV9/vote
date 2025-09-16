import azure.functions as func
import datetime, json, logging, uuid


app = func.FunctionApp()

@app.function_name(name="postUser")
@app.route(route="postUser", auth_level=func.AuthLevel.ANONYMOUS)
@app.cosmos_db_output(
    arg_name="outputDocument",
    connection="COSMOS_CONN_STRING",
    database_name="votedb",
    container_name="user",
    create_if_not_exists=True
)
def postUser(req: func.HttpRequest, outputDocument: func.Out[func.Document]) -> func.HttpResponse:
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