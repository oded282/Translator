import os
from redis import Redis, ConnectionError, DataError
from .logger import log
from transformers import MarianMTModel, MarianTokenizer
import data
from typing import Tuple

hostname = os.getenv("DB_HOSTNAME")
port = os.getenv("DB_PORT")
password = os.getenv("DB_PASSWORD")


class Operations:
    """Operations class with Operations inheritance

    """

    def __init__(self, set_name, database):
        self.set_name = set_name
        self.database = database
        self.conn = self.establish_connection()

    def connection(self) -> Redis:
        """Get Redis connection

        Returns:
            Redis: Redis instance
        """
        return Redis(host=hostname, port=port, password=password, db=self.database)

    def establish_connection(self) -> Redis:
        """Establish Redis successfuly connection or return False if failure.

        Returns:
            Redis: Redis instance
        """
        try:
            conn = self.connection()
            conn.ping()
        except ConnectionError:
            log.error("Connection to DB could not be established")
            return False
        return conn

    def insert(self, pairs: dict) -> None:
        """[Insert data as hash-map

        Args:
            pairs (dict): data as dictionary
        """
        if self.conn:
            try:
                self.conn.hset(self.set_name, None, None, pairs)
            except (DataError, ConnectionError):
                log.error("Error inserting data to database")
        else:
            log.error("Could not insert data to database, no connection")

    def get_all(self) -> dict:
        """Get all data from hash-map

        Returns:
            dict: data dictionary
        """
        try:
            return self.conn.hgetall(self.set_name)
        except ConnectionError:
            log.error("Could not get all data from database, no connection")

    def get_one(self, key: str) -> str:
        """Get one value by key

        Args:
            key (string): key

        Returns:
            [str]: value
        """
        try:
            value = self.conn.hget(self.set_name, key)
            if value:
                return value.decode("utf-8")
            log.info("Key does not exists in database")
            return ""
        except ConnectionError:
            log.error("Could not get data from database, no connection")

    def exists(self) -> bool:
        """Check if hash-map exists in database

        Returns:
            bool: True or False
        """
        if self.conn:
            return self.conn.exists(self.set_name)
        else:
            log.error("Could not check database existance, no connection")


class MyModel(Operations):
    def __init__(self, set_name, database):
        self.valid_transformations = [("en", "he"), ("he", "ru")]
        super().__init__(set_name, database)

    def is_valid_translation(self, src, tgt) -> bool:  # TODO Throw exception?
        if (src, tgt) in self.valid_transformations:
            return True
        else:
            return False
    
    def get_model(self, src_languae, tgt_language) -> Tuple:
        return data.models[f"Helsinki-NLP/opus-mt-{src_languae}-{tgt_language}"]

    def translate(self, src_languae, tgt_language, text) -> dict:
        if self.is_valid_translation(src_languae, tgt_language):
            value = super().get_one(f"{src_languae}{tgt_language}{text}")
            if value:
                return value

            src_texts = f">>{tgt_language}<< {text}"
            model, tokenizer = self.get_model(src_languae, tgt_language)
            translated = model.generate(**tokenizer.prepare_seq2seq_batch([src_texts]))
            tgt_text = tokenizer.decode(translated[0], skip_special_tokens=True)
            
            log.info(tgt_text)
            super().insert({f"{src_languae}{tgt_language}{text}": tgt_text})
            return tgt_text
        else:
            log.info("The given translation is not supported by the model")
            return []
