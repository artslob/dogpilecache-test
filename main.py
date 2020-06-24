from time import sleep

from dogpile.cache import make_region

region = make_region(name="users_region")


users = {str(i): f"user with id {i}" for i in range(1, 1000)}


def request_user(id):
    print(f"sleeping and requesting user {id}")
    sleep(5)
    return users[str(id)]


@region.cache_on_arguments(namespace="qwe", expiration_time=5)
def request_user_cached(id):
    return request_user(id)


def main():
    # simple cache on files:
    # region.configure(
    #     "dogpile.cache.dbm", expiration_time=300, arguments={"filename": "file.dbm"}
    # )
    region.configure(
        "dogpile.cache.redis",
        arguments={
            "host": "localhost",
            "port": 6379,
            "db": 0,
            "redis_expiration_time": 15,
            "distributed_lock": True,
            "thread_local_lock": False,
            "lock_sleep": 0.3,
        },
    )

    name = region.get_or_create(
        "7", request_user, expiration_time=5, creator_args=[("7",), {}]
    )
    print(name)
    result = region.get("7", expiration_time=50)
    print(result)

    print(request_user_cached("8"))
    print(request_user_cached("8"))
    print(request_user_cached("8"))

    print(region.get_multi(["7", "8", "9"]))
    print(region.get_multi(["7", "8", "9"]))


if __name__ == "__main__":
    main()
