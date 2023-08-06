import time
from http_session_redis import RedisStore


def test_store(redisdb):
    store = RedisStore(redisdb, 300)
    assert store.get('test') == {}
    store.set('test', {'this': 'is a session'})
    assert store.get('test') == {'this': 'is a session'}
    assert store.get('nothing') == {}


def test_timeout(redisdb):
    store = RedisStore(redisdb, 1)
    assert store.get('test') == {}
    store.set('test', {'this': 'is a session'})
    assert store.get('test') == {'this': 'is a session'}
    time.sleep(1)
    assert store.get('test') == {}


def test_touch(redisdb):
    store = RedisStore(redisdb, 2)
    assert store.get('test') == {}
    store.set('test', {'this': 'is a session'})
    assert store.get('test') == {'this': 'is a session'}
    time.sleep(1)
    store.touch('test')
    time.sleep(1)
    assert store.get('test') == {'this': 'is a session'}
    time.sleep(1)
    assert store.get('test') == {}
