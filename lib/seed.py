#!/usr/bin/env python3

# Script goes here!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie, Base

# database engine
engine = create_engine('sqlite:///freebies.db')

# for the tables
Base.metadata.create_all(engine)

# a new session
Session = sessionmaker(bind=engine)
session = Session()

# the different companies
company1 = Company(name="Google", founding_year=1998)
company2 = Company(name="Microsoft", founding_year=1975)

# the different devs
dev1 = Dev(name="Paul")
dev2 = Dev(name="Anita")

#the different freebies
freebie1 = Freebie(item_name="T-shirt", value=5, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Mug", value=7, dev=dev2, company=company2)

#session and commit
session.add_all([company1, company2, dev1, dev2, freebie1, freebie2])
session.commit()

print("Successful Database data")
