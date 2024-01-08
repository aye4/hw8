from models import Author, Quote

s = "1-2-3-4"
print(s.split('-'))
print(s.split('-', 1))
x, *y = s.split(":", 1)
print(x, y)


print([author.fullname for author in Author.objects()])
print([quote.quote for quotes in Author.objects()])