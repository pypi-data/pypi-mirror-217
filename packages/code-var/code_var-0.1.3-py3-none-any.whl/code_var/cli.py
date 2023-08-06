import typer
import requests
from bs4 import BeautifulSoup

app = typer.Typer()


@app.command()
def name(keyword):
    params = {
        'word': f'{keyword}',
    }
    response = requests.get('https://www.chtml.cn/w', params=params)
    page = BeautifulSoup(response.text, features="html.parser")
    var_text = ''
    for p in page.find_all('p')[1:9]:
        var_text += (p.text + '\n')

    typer.echo(var_text)


def run():
    app()
