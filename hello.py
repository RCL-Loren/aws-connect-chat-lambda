import boto3
import asyncio
import websockets
import ssl

def handler(event, context):
    client = boto3.client('connect')

    response = client.start_chat_contact(
        InstanceId='97f8364a-b438-489e-bc27-241e3210f694',
        ContactFlowId='0ecd1ecd-734a-4250-9b1c-c07409438adc',
        Attributes={
            'string': 'string'
        },
        ParticipantDetails={
            'DisplayName': 'Test User'
        },
        InitialMessage={
            'ContentType': 'text/plain',
            'Content': 'Hi there'
        },
    )

    ptoken = response['ParticipantToken'] 

    participant_client = boto3.client('connectparticipant')

    response = participant_client.create_participant_connection(
        Type=['WEBSOCKET',
        ],
        ParticipantToken=ptoken
    )

    mysocket = response['Websocket']['Url']

    async def hello(uri):
        async with websockets.connect(
            uri, ssl=True
        ) as websocket:

            topic = '{"topic":"aws/subscribe","content":{"topics":["aws/chat"]}}'
            await websocket.send(topic)

            name = 'test'

           # await websocket.send(name)
           # print("> {}".format(name))

           # greeting = await websocket.recv()
           # print("< {}".format(greeting))

    asyncio.get_event_loop().run_until_complete(hello(mysocket))

    return {"message": "hi there"}
    

