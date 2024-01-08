import re
import redis
from redis_lru import RedisLRU
from models import Author, Quote


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def get_quotes_by_author(name: str) -> str:
    author = Author.objects(fullname__istartswith=name).first()
    if not author:
        return f"\nNo matches found for the name '{name}'\n"
    quotes = Quote.objects(author=author)
    if not quotes:
        return f"\nNo quotes found for '{author.fullname}'\n"
    return (
        "\n".join(
            [f"\nQuotes by {author.fullname}:"] +
            ["-" * 10] +
            [quote.quote + "\n" + str(quote.tags) for quote in quotes]
        )
    )


@cache
def get_quotes_by_tags(tags: list[str] | str) -> str:
    if isinstance(tags, list) and len(tags) > 1:
        quotes = Quote.objects(tags__in=tags)
    elif isinstance(tags, str):
        quotes = Quote.objects(
            tags=re.compile(fr'^{tags}', flags=re.IGNORECASE)
        )
    else:
        quotes = Quote.objects(
            tags=re.compile(fr'^{tags[0]}', flags=re.IGNORECASE)
        )
    if not quotes:
        return f"\nNo quotes found for tag(s) '{tags}'\n"
    return (
        "\n".join([
            "\n" + quote.author.fullname +
            "\n" + quote.quote +
            "\n" + str(quote.tags)
            for quote in quotes
        ])
    )


def print_intro():
    print("Welcome to the Quotes!\n" + "-" * 20)
    print("Available commands are:")
    print("name:<author>")
    print("tag:<tag>")
    print("tags:<tag1,tag2...>")
    print("exit\n" + "-" * 20)


def main():
    print_intro()
    while True:
        command, *args = input("\nEnter command: ").lower().split(":", 1)
        if command == "exit":
            print("\nGood buy!")
            break
        elif not args:
            result = "\nNo arguments specified\n"
        elif command == "name":
            result = get_quotes_by_author(args[0])
        elif command == "tag":
            result = get_quotes_by_tags(args[0])
        elif command == "tags":
            result = get_quotes_by_tags(args[0].split(','))
        else:
            result = f"\nUnrecognized command '{command}'\n"
        print(result)


if __name__ == '__main__':
    main()
