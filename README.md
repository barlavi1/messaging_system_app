# messaging system app
This is a simple rest API backend system that is responsible for handling
messages between users.
a message contains :
1. sender (owner)
2. Receiver
3. Message
4. Subject
5. creation date

## Functionalities
* Write message
* Get all messages for a specific user
* Get all unread messages for a specific user
* Read message (return one message)
* Delete message (as owner or as receiver)

## API:
### Prolog
To send a REST request, you need a username and password on the server.
A username and password can be set only by the Admin, using the Admin UI.
Every request needs to hold in the Authorization a Bearer and a Token.
Example, a GET request:
```
curl -H 'Authorization: Bearer <access token>' -X GET <server_address>:<port>/<request_route>
```

### Routes

| Route | Request Type Allowed | Payload | Details |
| ----- | -------------------- | ------- | ------- |
| /api/get_token/ | POST | {username: str, password: str} | get access token and refresh token |
| /api/token_refresh | POST | { refresh: str } | refresh expired access token |
| /api/message/ | POST | 'subject': 'subject of the message','message': 'content of the message', 'receiver' : id of the receiver | creates a new message and saves it as "unread" with timestamp |
| /api/message/<id>/ | GET | | read a message | 
| /api/message/<id>/ | DELETE | | remove a message |
| /api/all_messages/ | GET | | read all messages and mark them as "read" |
| /api/unread_messages/ | GET | | read all unread messages and mark them as "read" |





