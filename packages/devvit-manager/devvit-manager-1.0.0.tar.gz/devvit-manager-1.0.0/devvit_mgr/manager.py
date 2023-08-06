"""Provide the Manager class."""
from __future__ import annotations

import json

from click import secho, style

from .const import PROFILES_FILE, TOKEN_PATH
from .models import Profile


class Manager:
    """Manage user accounts."""

    @property
    def active_profile(self) -> Profile | None:
        """Get the active profile."""
        for profile in self.profiles.values():
            if profile.active:
                return profile
        return None

    @staticmethod
    def _load() -> dict[str, Profile]:
        """Load the config file."""
        if not PROFILES_FILE.exists():
            PROFILES_FILE.parent.mkdir(parents=True, exist_ok=True)
            PROFILES_FILE.write_text("{}")
            return {}
        with PROFILES_FILE.open() as f:
            return Profile.from_dict(json.load(f))

    def __init__(self) -> None:
        """Initialize the Manager class."""
        self.profiles: dict[str, Profile] = self._load()
        self.add_profile()

    def _save(self):
        """Save the config file."""
        with PROFILES_FILE.open("w") as f:
            json.dump({k: v.token_data for k, v in self.profiles.items()}, f, indent=4)

    def add_profile(self):
        """Add a profile."""
        if TOKEN_PATH.exists():
            with TOKEN_PATH.open() as f:
                profile = Profile(json.load(f))
                if profile.username:
                    self.profiles[profile.username] = profile
                    self._save()

    def switch_profile(self, profile: str):
        """Switch to a profile."""
        if profile not in self.profiles:
            secho(
                f"No profile exists for {style(f'u/{profile}', fg='blue')}",
                fg="red",
            )
            return
        profile = self.profiles[profile]
        with TOKEN_PATH.open("w") as f:
            json.dump(profile.token_data, f)
        secho(f"Switched to {style(f'u/{profile.username}', fg='blue')}", fg="green")

    def remove_profile(self, profile: str):
        """Remove a profile."""
        if profile not in self.profiles:
            secho(
                f"No profile exists for {style(f'u/{profile}', fg='blue')}",
                fg="red",
            )
            return
        if self.profiles[profile].active:
            TOKEN_PATH.unlink()
        del self.profiles[profile]
        self._save()
        secho(
            f"Successfully removed profile for {style(f'u/{profile}', fg='blue')}",
            fg="green",
        )
