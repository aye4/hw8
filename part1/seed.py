from models import Author, Quote
import json


def read_json(file_path) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            exit(f"Could not decode '{file_path}'")


if __name__ == "__main__":
    authors_source = read_json("authors.json")
    quotes_source = read_json("quotes.json")
    for author in authors_source:
        if not Author.objects(fullname=author.get("fullname")):
            Author(**author).save()
        else:
            print(f"{author['fullname']} had already been registered")
    for quote in quotes_source:
        fullname = quote.get("author")
        author = Author.objects(fullname=fullname).first()
        if author:
            if not Quote.objects(quote=quote.get("quote")):
                Quote(
                    tags=quote.get("tags"),
                    author=author,
                    quote=quote.get("quote")
                ).save()
            else:
                print(f"Quote by {author.fullname} {quote['quote']} "
                      f"had already been saved")
        else:
            print(
                f"Could not find the author '{fullname}' for quote:\n"
                f"{quote['quote']}"
            )
