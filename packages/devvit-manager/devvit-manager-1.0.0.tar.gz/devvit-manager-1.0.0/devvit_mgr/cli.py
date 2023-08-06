"""Provides the CLI for the devvit-manager package."""
from subprocess import check_call

import click
import pick
from click import Context, confirm, secho, style

from .const import TOKEN_PATH
from .manager import Manager


def build_options(manager: Manager) -> list[str]:
    """Build the options for the pick menu."""
    return [
        f"{k} (signed in)" if v.active else k for k, v in manager.profiles.items()
    ] + ["Cancel"]


@click.group()
@click.pass_context
def main(context: Context):
    """Entry point for the application script."""
    context.obj = Manager()


@main.command()
@click.pass_obj
def login(manager: Manager):
    """Sign in to devvit."""
    if TOKEN_PATH.exists():
        if manager.active_profile:
            secho(
                f"You are already signed in as {style(f'u/{manager.active_profile.username}', fg='blue')}",
                fg="yellow",
            )
            confirm(
                "Do you want to sign out? This is needed to sign in to another profile.",
                default=False,
            )
        code = check_call(["devvit", "logout"])
        if code != 0:
            secho("Failed to sign out.", fg="red")
            return
    code = check_call(["devvit", "login"])
    if code != 0:
        secho("Failed to log in.", fg="red")
        return
    manager.add_profile()


@main.command()
@click.pass_obj
@click.argument("profile", required=False)
def remove_profile(manager: Manager, profile: str = None):
    """Remove a profile."""
    if not profile:
        profile, _ = pick.pick(
            build_options(manager),
            "Please which profile to remove (This will also sign you out from devvit if it is the active profile):",
            indicator="→",
            default_index=0,
        )
        if profile == "Cancel":
            return
    manager.remove_profile(profile.split()[0])


@main.command()
@click.pass_obj
@click.argument("profile", required=False)
def switch(manager, profile: str = None):
    """Switch to a different Reddit account."""
    if not profile:
        profile, _ = pick.pick(
            build_options(manager),
            "Please which profile to switch to:",
            indicator="→",
            default_index=0,
        )
        if profile == "Cancel":
            return
    profiles = manager.profiles
    if not profiles:
        secho(
            f"No profiles saved. Use {style('devvit login', fg='yellow')} first.",
            fg="red",
        )
        return
    manager.switch_profile(profile.split()[0])
