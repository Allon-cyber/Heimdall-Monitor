from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Define the base for our declarative models
Base = declarative_base()

# Define the SystemMetric model
class SystemMetric(Base):
    __tablename__ = 'system_metrics'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    process_count = Column(Integer)
    active_network_connections = Column(Integer)

    def __repr__(self):
        return (f"<SystemMetric(timestamp='{self.timestamp}', cpu_percent={self.cpu_percent}, "
                f"memory_percent={self.memory_percent}, process_count={self.process_count}, "
                f"active_network_connections={self.active_network_connections})>")

# Database setup
DATABASE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'monitoring_data.sqlite')
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initializes the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_metric(cpu_percent, memory_percent, process_count, active_network_connections):
    """Saves a single system metric record to the database."""
    db = SessionLocal()
    try:
        metric = SystemMetric(
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            process_count=process_count,
            active_network_connections=active_network_connections
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure the data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    init_db()
    print(f"Database initialized at {DATABASE_FILE}")
    # Example usage:
    save_metric(50.5, 70.2, 150, 25)
    print("Example metric saved.")
