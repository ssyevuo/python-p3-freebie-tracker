from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database engine and session
engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    founding_year = Column(Integer(), nullable=False)

    # a company has many freebies
    freebies = relationship("Freebie", back_populates="company")

    # a company gives freebies to multiple devs
    devs = relationship("Dev", secondary="freebies", back_populates="companies", overlaps="freebies,devs")

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        new_freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(new_freebie)
        session.commit()

    @classmethod
    def oldest_company(cls):
        return session.query(cls).order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String(), nullable=False)

    #a dev can receive many freebies
    freebies = relationship("Freebie", back_populates="dev")

    # a dev can receive freebies from multiple companies
    companies = relationship("Company", secondary="freebies", back_populates="devs", overlaps="freebies,devs")

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)
    
    def give_away(self, dev, freebie):
        if freebie in self.freebies:
            freebie.dev = dev
            session.commit()
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    value = Column(Integer, nullable=False)
    dev_id = Column(Integer, ForeignKey('devs.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    # the relationships
    dev = relationship("Dev", back_populates="freebies", overlaps="companies,devs")
    company = relationship("Company", back_populates="freebies", overlaps="companies,devs")

    def __repr__(self):
        return f'<Freebie {self.item_name} (${self.value})>'
    
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}."
    
