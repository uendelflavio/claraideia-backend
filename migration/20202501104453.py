"""
Initial migration

Adds 1000 numbers to numbers collection.
"""
name = "20150612230153"
dependencies = []


def upgrade(db):
    db.users.insert_one({
        "username" : "uendel",
        "email" : "uendel@mail.com",
        "bio" : "",
        "image" : "",
        "created_at" : "2018-12-25T02:16:16.000Z",
        "updated_at" : "2018-12-25T02:16:16.000Z",
        "salt" : "$2b$12$hzJfGIpqoRFIfai1wSdVKe",
        "hashed_password" : "$2b$12$QSBqzFW4M/fUfqt1B01rUOwTBrd6BQJCZBTg5wBbV/Sup464w7r/u"
    })
    db.sensors.insert_one({
        "description" : "DHT11",
        "data_reading" : "2020-01-23T09:29:43.234Z",
        "reading" : "2020-01-23T09:29:43.234Z",
        "createdAt" : "2020-01-23T09:38:55.123Z",
        "updatedAt" : "2020-01-23T09:38:55.123Z"
    })
    db.stations.insert_one({
        "station_name": "STA001",      
        "location" : {
              "type" : "Point",
              "coordinates" : [
                  -120.24,
                  39.21
              ]
        } 
    })
    db.employer.insert_one({
        "social_reason": "faz.sao joao",
        "contract": "comodato",
        "cpf_cnpj":"795.136.25.14"
    })


def downgrade(db):
    db.users.drop() 
    db.sensors.drop()
    db.stations.drop()
    db.employer.drop()
               