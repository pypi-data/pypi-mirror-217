from fzf import fzf_prompt

english = ["actvid", "sflix", "solar", "dopebox", "openloadmov", "remotestream"]

# german = ["kinox"] kinox was removed, as it didn't function really.

indian = [
    "streamblasters",
    "tamilyogi",
    "einthusan",
]

asian = [
    "viewasian",
    "watchasian",
]

anime = ["gogoanime", "animefox"]

tv = ["eja"]

cartoons = ["kisscartoon"]

turkish = ["turkish123", "yoturkish"]

sports = ["scdn"]

update = ["pip install mov-cli -U"]

inter = [
    "wlext",
]

preselction = {
    "English Providers": [english],
    "Indian Providers": [indian],
    "Asian Providers": [asian],
    "LIVE TV Providers": [tv],
    "Cartoons Providers": [cartoons],
    "Turkish Providers": [turkish],
    "Anime Providers": [anime],
    "Sports Providers": [sports],
    "International Providers": [inter],
}


def ask():
    init = fzf_prompt(preselction)
    get = preselction.get(init)[0]
    choice = fzf_prompt(get)
    return choice
