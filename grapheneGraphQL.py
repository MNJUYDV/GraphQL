import graphene
from graphene import ObjectType, String, List, Int

# Define the Author and Book data models
class Author(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    books = List(lambda: Book)

class Book(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    author = graphene.Field(Author)

# Create data for authors and books (for demonstration)
authors_data = [
    {'id': 1, 'name': 'John Doe'},
    {'id': 2, 'name': 'Jane Smith'},
]

books_data = [
    {'id': 1, 'title': 'GraphQL for Beginners', 'author_id': 1},
    {'id': 2, 'title': 'Advanced GraphQL', 'author_id': 2},
    {'id': 3, 'title': 'Python Programming', 'author_id': 1},
]

# Query to fetch a single author by ID
class Query(ObjectType):
    author = graphene.Field(Author, id=Int())
    
    def resolve_author(self, info, id):
        for author in authors_data:
            if author['id'] == id:
                return Author(id=author['id'], name=author['name'])
        return None

# Query to fetch all authors
class Query(ObjectType):
    all_authors = List(Author)
    
    def resolve_all_authors(self, info):
        return [Author(id=author['id'], name=author['name']) for author in authors_data]

# Query to fetch a single book by ID
class Query(ObjectType):
    book = graphene.Field(Book, id=Int())
    
    def resolve_book(self, info, id):
        for book in books_data:
            if book['id'] == id:
                author_id = book['author_id']
                author = next(author for author in authors_data if author['id'] == author_id)
                return Book(id=book['id'], title=book['title'], author=Author(id=author['id'], name=author['name']))
        return None

# Query to fetch all books
class Query(ObjectType):
    all_books = List(Book)
    
    def resolve_all_books(self, info):
        return [Book(id=book['id'], title=book['title'], author=Author(id=book['author_id'], name='')) for book in books_data]

# Create the GraphQL schema
schema = graphene.Schema(query=Query)

# Define a mutation for creating a new book
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        author_id = graphene.Int()

    book = graphene.Field(Book)

    def mutate(self, info, title, author_id):
        new_book = {'id': len(books_data) + 1, 'title': title, 'author_id': author_id}
        books_data.append(new_book)
        author = next(author for author in authors_data if author['id'] == author_id)
        return CreateBook(book=Book(id=new_book['id'], title=title, author=Author(id=author_id, name=author['name'])))

# Define a mutation for creating a new author
class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    author = graphene.Field(Author)

    def mutate(self, info, name):
        new_author = {'id': len(authors_data) + 1, 'name': name}
        authors_data.append(new_author)
        return CreateAuthor(author=Author(id=new_author['id'], name=name))

# Define a mutation for deleting a book by ID
class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        global books_data
        books_data = [book for book in books_data if book['id'] != id]
        return DeleteBook(success=True)

# Define a mutation for deleting an author by ID
class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate(self, info, id):
        global authors_data
        authors_data = [author for author in authors_data if author['id'] != id]
        return DeleteAuthor(success=True)

# Create the GraphQL mutations
class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    create_author = CreateAuthor.Field()
    delete_book = DeleteBook.Field()
    delete_author = DeleteAuthor.Field()

# Add the mutations to the schema
schema = graphene.Schema(query=Query, mutation=Mutation)

# Sample query for testing
query = """
mutation {
    createAuthor(name: "Alice Johnson") {
        author {
            id
            name
        }
    }
}
"""

if __name__ == "__main__":
    result = schema.execute(query)
    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(error)
    else:
        print("Data:")
        print(result.data)
