import click
import asyncio
from jolted_mod import create_notebook_module, create_wiki_module
import nbformat as nbf


@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--interactive", "-i", is_flag=True, default=False, help="Interactive mode."
)
@click.option("--topic", required=False, type=str, help="The topic for the module.")
@click.option(
    "--identity",
    default="professor of computer science",
    type=str,
    help="The identity of the content creator.",
)
@click.option(
    "--educational-background",
    default="Computer Science Undergraduate",
    type=str,
    help="The educational background of the target audience.",
)
@click.option(
    "--level-of-expertise",
    default="Beginner",
    type=str,
    help="The level of expertise of the target audience.",
)
@click.option(
    "--is-code",
    default=True,
    type=bool,
    help="Whether the module should include code or not.",
)
@click.option(
    "--model",
    default="gpt-4",
    type=str,
    help="The AI model used for content generation.",
)
def create_notebook(
    interactive,
    topic,
    identity,
    educational_background,
    level_of_expertise,
    is_code,
    model,
):
    """
    Creates a notebook module based on the provided topic.
    """
    if interactive:
        topic = click.prompt("Please enter the topic for the module", type=str)
        identity = click.prompt(
            "Please enter the identity of the content creator",
            type=str,
            default="professor of computer science",
        )
        educational_background = click.prompt(
            "Please enter the educational background of the target audience",
            type=str,
            default="Computer Science Undergraduate",
        )
        level_of_expertise = click.prompt(
            "Please enter the level of expertise of the target audience",
            type=str,
            default="Beginner",
        )
        model = click.prompt(
            "Please enter the AI model used for content generation",
            type=str,
            default="gpt-4",
        )

    tutorial_content = asyncio.run(
        create_notebook_module(
            topic=topic,
            identity=identity,
            target_audience=f"students with {educational_background} and {level_of_expertise}",
            is_code=is_code,
            model=model,
        )
    )
    nbf.write(tutorial_content, f"{topic}.ipynb")
    click.echo(f"Created {topic}.ipynb")


@click.command()
@click.option("--topic", required=True, type=str, help="The topic for the module.")
@click.option(
    "--identity",
    default="professor of computer science",
    type=str,
    help="The identity of the content creator.",
)
@click.option(
    "--target-audience",
    default="first year computer science students",
    type=str,
    help="The target audience of the module.",
)
@click.option(
    "--is-code",
    default=True,
    type=bool,
    help="Whether the module should include code or not.",
)
@click.option(
    "--model",
    default="gpt-3.5-turbo",
    type=str,
    help="The AI model used for content generation.",
)
def create_wiki(
    topic: str, identity: str, target_audience: str, is_code: bool, model: str
):
    """
    Creates a wiki module based on the provided topic.
    """
    wiki_content = asyncio.run(
        create_wiki_module(topic, identity, target_audience, is_code, model)
    )
    click.echo(wiki_content)


cli.add_command(create_notebook)
cli.add_command(create_wiki)


if __name__ == "__main__":
    cli()
