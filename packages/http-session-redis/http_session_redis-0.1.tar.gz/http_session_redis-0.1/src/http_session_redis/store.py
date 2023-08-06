import redis
import typing as t
from datetime import timedelta
from http_session.meta import Store, SessionData
from cromlech.marshallers import Marshaller, PickleMarshaller


class RedisStore(Store):
    """Redis based HTTP session.
    """

    def __init__(self,
                 redis: redis.Redis,
                 delta: int,
                 prefix: str = 'session:',
                 marshaller: t.Type[Marshaller] = PickleMarshaller):
        self.delta = delta  # timedelta in seconds.
        self.redis = redis
        self.marshaller = marshaller
        self.prefix = prefix

    def __iter__(self):
        for key in self.redis.scan_iter(f'{self.prefix}%s*'):
            yield str(key[len(self.prefix):], 'utf-8')

    def get(self, sid: str) -> SessionData:
        key = self.prefix + sid
        data = self.redis.get(key)
        if data is None:
            return self.new()
        session = self.marshaller.loads(data)
        return session

    def set(self, sid: str, session: SessionData):
        key = self.prefix + sid
        data = self.marshaller.dumps(session)
        self.redis.setex(key, timedelta(seconds=self.delta), data)

    def clear(self, sid: str):
        key = self.prefix + sid
        self.redis.delete(key)

    delete = clear

    def touch(self, sid: str):
        key = self.prefix + sid
        self.redis.expire(key, timedelta(seconds=self.delta))

    def new(self) -> t.Dict:
        return {}
