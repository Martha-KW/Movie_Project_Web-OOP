import os
from movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from user_manager import UserManager

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Movie Collection</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ color: #333; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Movie Collection</h1>
    {content}
</body>
</html>
"""

def generate_html():
    """This generates a simple static website to display the content of the
    personal movie database The generation is started in the CLI.
    """
    user_manager = UserManager()

    if not user_manager.users:
        content = "<p>No users found. Please register first.</p>"
    else:
        username = next(iter(user_manager.users))
        user_data = user_manager.users[username]
        file_type = user_data["format"]
        file_name = user_data["file"]

        try:
            if file_type == "json":
                storage = StorageJson(file_name)
            else:
                storage = StorageCsv(file_name)
        except FileNotFoundError:
            content = f"<p>Error: {file_name} not found in data/ directory.</p>"
        else:
            movie_app = MovieApp(storage)
            movies = movie_app.get_movies()

            if not movies:
                content = "<p>No movies found.</p>"
            else:
                table_rows = "".join(
                    f"<tr><td>{m['title']}</td><td>{m['year']}</td><td>{m['rating']}</td><td>{m['notes']}</td></tr>"
                    for m in movies
                )
                content = f"""
                <table>
                    <tr><th>Title</th><th>Year</th><th>Rating</th><th>Notes</th></tr>
                    {table_rows}
                </table>
                """

    html = HTML_TEMPLATE.format(content=content)

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("HTML page generated: output/index.html")


if __name__ == "__main__":
    generate_html()
