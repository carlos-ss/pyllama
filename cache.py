from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime
import hashlib
from pathlib import Path
import os

from llm import PyLlama

Base = declarative_base()

class CacheEntry(Base):
    __tablename__ = 'cache'
    id = Column(String(32), primary_key=True)
    prompt = Column(Text, unique=True)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CacheManager:

    def __init__(self):
        self.cache_dir = Path(__file__).parent / ".cache" / "llama_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{self.cache_dir/'cache.db'}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def _hash_prompt(self, prompt: str) -> str: 
        """Hash the prompt to create a unique identifier."""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def get_response(self, prompt: str) -> str:
        prompt_hash = self._hash_prompt(prompt)
        print(f"Prompt hash: {prompt_hash}")
        with self.Session() as session:
            
            # check if the prompt is already in the cache 
            if entry:= session.query(CacheEntry).get(prompt_hash):
                print(f"Cache hit for prompt: {prompt_hash}")
                return entry.response
            
            #  cache miss
            print(f"Cache miss for prompt: {prompt_hash}")
            llm = PyLlama()
            llm.ask_ai(prompt)
            session.add(CacheEntry(id=prompt_hash, prompt=prompt, response=llm.response))
            session.commit()
            print(f"Added to cache: {prompt_hash}")
            return llm.response
            
        
    def add_to_cache(self, prompt: str, response: str):
        with self.Session() as session:
            entry = CacheEntry(prompt=prompt, response=response)
            session.add(entry)
            session.commit()
            print(f"Added to cache: {prompt}")
            print(f"Response: {response}")