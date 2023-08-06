
## Get Started


```python
class MyTable(Base):  # Replace 'Base' with your declarative base class
    __tablename__ = 'my_table'
    id = Column(ULIDType, primary_key=True, server_default=text("gen_monotonic_ulid()"))
```