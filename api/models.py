from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, CHAR, UniqueConstraint

class Base(DeclarativeBase):
    pass

class SampleData(Base):
    __tablename__ = "sample_data"

    id:        Mapped[int]    = mapped_column(Integer, primary_key=True)
    first_name:Mapped[str]    = mapped_column(String(100), nullable=False)
    last_name: Mapped[str]    = mapped_column(String(100), nullable=False)
    company_name:Mapped[str]  = mapped_column(String(255))
    address:   Mapped[str]    = mapped_column(Text)
    city:      Mapped[str]    = mapped_column(String(100))
    state:     Mapped[str]    = mapped_column(CHAR(2), nullable=False)
    zip:       Mapped[str]    = mapped_column(String(10))
    phone1:    Mapped[str]    = mapped_column(String(20))
    phone2:    Mapped[str]    = mapped_column(String(20))
    email:     Mapped[str]    = mapped_column(String(255))
    department:Mapped[str]    = mapped_column(String(100))

    __table_args__ = (
        UniqueConstraint('first_name', 'last_name', 'email', 'department', name='uq_sample'),
    )
    def __repr__(self):
        return f"<SampleData(id={self.id}, first_name='{self.first_name}', last_name='{self.last_name}')>"