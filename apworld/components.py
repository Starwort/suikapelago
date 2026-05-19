import webbrowser

from worlds.LauncherComponents import Component, Type, components, icon_paths


def run_client(*args: str) -> None:
    webbrowser.open("https://starwort.github.io/suikapelago/")


icon_paths["Suikapelago"] = "ap:worlds.suikapelago/icon.png"

components.append(
    Component(
        "Suikapelago Client",
        func=run_client,
        game_name="Suikapelago",
        icon="Suikapelago",
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)
