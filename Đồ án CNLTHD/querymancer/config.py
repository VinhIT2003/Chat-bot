import os
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import pyodbc

class ModelProvider(str, Enum):
    OLLAMA="ollama"
    GROQ="groq"

@dataclass
class ModelConfig:
    name: str
    temperature: float
    provider: ModelProvider

QWEN_2_5 = ModelConfig("qwen2.5", 0.0, ModelProvider.OLLAMA)
GEMMA_3 = ModelConfig("PetrosStav/gemma3-tools:12b", 0.7, ModelProvider.OLLAMA)
LLAMA_3_3 = ModelConfig("llama-3.3-70b-versatile", 0.0, ModelProvider.OLLAMA)

class Config:
    SEED = 42
    MODEL = QWEN_2_5
    OLLAMA_CONTEXT_WINDOW = 2048


    def connect_db():
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=YONORIKOMANA\\QUOCDUONG;'
            'DATABASE=test;'
            'UID=sa;PWD=1234;Encrypt=no'
        )
        return conn

def seed_everything(seed: int = Config.SEED):
    random.seed(seed_everything)


    #python -m streamlit run querymancer/app.py